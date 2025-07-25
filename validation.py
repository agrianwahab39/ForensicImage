"""
Image validation and preprocessing functions
"""

import os
import numpy as np
from PIL import Image, ImageEnhance
import cv2
import exifread
from datetime import datetime
from config import VALID_EXTENSIONS, MIN_FILE_SIZE, TARGET_MAX_DIM

def validate_image_file(filepath):
    """Enhanced validation with more format support"""
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in VALID_EXTENSIONS:
        raise ValueError(f"Format file tidak didukung: {ext}")
    
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File {filepath} tidak ditemukan.")
    
    file_size = os.path.getsize(filepath)
    if file_size < MIN_FILE_SIZE:
        print(f"⚠ Warning: File sangat kecil ({file_size} bytes), hasil mungkin kurang akurat")
    
    return True

def extract_enhanced_metadata(filepath):
    """Enhanced metadata extraction dengan analisis inkonsistensi yang lebih detail"""
    metadata = {}
    try:
        with open(filepath, 'rb') as f:
            tags = exifread.process_file(f, details=False, strict=False)
        
        metadata['Filename'] = os.path.basename(filepath)
        metadata['FileSize (bytes)'] = os.path.getsize(filepath)
        
        try:
            metadata['LastModified'] = datetime.fromtimestamp(
                os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            metadata['LastModified'] = str(os.path.getmtime(filepath))
        
        # Extract comprehensive EXIF tags
        comprehensive_tags = [
            'Image DateTime', 'EXIF DateTimeOriginal', 'EXIF DateTimeDigitized',
            'Image Software', 'Image Make', 'Image Model', 'Image ImageWidth',
            'Image ImageLength', 'EXIF ExifVersion', 'EXIF ColorSpace',
            'Image Orientation', 'EXIF Flash', 'EXIF WhiteBalance',
            'GPS GPSLatitudeRef', 'GPS GPSLatitude', 'GPS GPSLongitudeRef',
            'EXIF LensModel', 'EXIF FocalLength', 'EXIF ISO', 'EXIF ExposureTime'
        ]
        
        for tag in comprehensive_tags:
            if tag in tags:
                metadata[tag] = str(tags[tag])
        
        metadata['Metadata_Inconsistency'] = check_enhanced_metadata_consistency(tags)
        metadata['Metadata_Authenticity_Score'] = calculate_metadata_authenticity_score(tags)
        
    except Exception as e:
        print(f"⚠ Peringatan: Gagal membaca metadata EXIF: {e}")
    
    return metadata

def check_enhanced_metadata_consistency(tags):
    """Enhanced metadata consistency check"""
    inconsistencies = []
    
    # Time consistency check
    datetime_tags = ['Image DateTime', 'EXIF DateTimeOriginal', 'EXIF DateTimeDigitized']
    datetimes = []
    
    for tag in datetime_tags:
        if tag in tags:
            try:
                dt_str = str(tags[tag])
                dt = datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S')
                datetimes.append((tag, dt))
            except:
                pass
    
    if len(datetimes) > 1:
        for i in range(len(datetimes)-1):
            for j in range(i+1, len(datetimes)):
                diff = abs((datetimes[i][1] - datetimes[j][1]).total_seconds())
                if diff > 60:  # 1 minute
                    inconsistencies.append(f"Time difference: {datetimes[i][0]} vs {datetimes[j][0]} ({diff:.0f}s)")
    
    # Software signature check
    if 'Image Software' in tags:
        software = str(tags['Image Software']).lower()
        suspicious_software = ['photoshop', 'gimp', 'paint', 'editor', 'modified']
        if any(sus in software for sus in suspicious_software):
            inconsistencies.append(f"Editing software detected: {software}")
    
    return inconsistencies

def calculate_metadata_authenticity_score(tags):
    """Calculate metadata authenticity score (0-100)"""
    score = 100
    
    # Penalty for missing essential metadata
    essential_tags = ['Image DateTime', 'Image Make', 'Image Model']
    missing_count = sum(1 for tag in essential_tags if tag not in tags)
    score -= missing_count * 15
    
    # Penalty for editing software
    if 'Image Software' in tags:
        software = str(tags['Image Software']).lower()
        if any(sus in software for sus in ['photoshop', 'gimp', 'paint']):
            score -= 30
    
    # Bonus for complete metadata
    all_tags = len([tag for tag in tags if str(tag).startswith(('Image', 'EXIF', 'GPS'))])
    if all_tags > 20:
        score += 10
    
    return max(0, min(100, score))

def advanced_preprocess_image(image_pil, target_max_dim=TARGET_MAX_DIM):
    """Advanced preprocessing dengan enhancement dan size optimization"""
    if image_pil.mode != 'RGB':
        image_pil = image_pil.convert('RGB')
    
    original_width, original_height = image_pil.size
    print(f"  Original size: {original_width} × {original_height}")
    
    # More aggressive resizing for very large images
    if original_width > target_max_dim or original_height > target_max_dim:
        ratio = min(target_max_dim/original_width, target_max_dim/original_height)
        new_size = (int(original_width * ratio), int(original_height * ratio))
        image_pil = image_pil.resize(new_size, Image.Resampling.LANCZOS)
        print(f"  Resized to: {new_size[0]} × {new_size[1]} (ratio: {ratio:.3f})")
    
    # Light denoising for smaller images only
    if max(image_pil.size) <= 2000:
        image_array = np.array(image_pil)
        denoised = cv2.fastNlMeansDenoisingColored(image_array, None, 3, 3, 7, 21)
        return Image.fromarray(denoised), image_pil
    else:
        print("  Skipping denoising for large image")
        return image_pil, image_pil
