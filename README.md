# Sistem Forensik Gambar

Sistem ini merupakan kumpulan skrip Python untuk melakukan analisis forensik pada gambar digital. Berbagai modul disediakan untuk mendeteksi indikasi pemalsuan seperti **copy–move**, **splicing**, hingga manipulasi kompleks. Proses analisis mengombinasikan metode Error Level Analysis (ELA), pendeteksian fitur, analisis noise, tekstur, iluminasi, serta klasifikasi berbasis machine learning.

## Fitur Utama

- **Validasi & Preproses** – Pengecekan format file, ekstraksi metadata yang diperluas, dan pra‑pemrosesan gambar.
- **Error Level Analysis** – `ela_analysis.py` menghasilkan peta ELA pada berbagai level kompresi serta statistik regional.
- **Deteksi Copy‑Move** – `feature_detection.py` dan `copy_move_detection.py` menyediakan deteksi berbasis fitur (SIFT/ORB/AKAZE) serta metode block matching.
- **Analisis Lanjutan** – `advanced_analysis.py` berisi analisis noise, domain frekuensi (DCT), tekstur (GLCM/LBP), edge, iluminasi, dan statistik warna.
- **Analisis JPEG & Ghost** – `jpeg_analysis.py` mengevaluasi artefak kompresi dan mendeteksi indikasi double compression menggunakan JPEG ghost analysis.
- **Klasifikasi Manipulasi** – `classification.py` menghitung feature vector dan memperkirakan skor manipulasi (copy‑move, splicing) dengan beberapa model ML.
- **Visualisasi & Ekspor** – `visualization.py` membuat laporan visual komprehensif. `export_utils.py` memungkinkan ekspor ke PNG, PDF, dan DOCX.
- **Antarmuka Web** – `app2.py` menyediakan aplikasi Streamlit untuk penggunaan interaktif.
- **Riwayat Analisis** – Hasil ringkas disimpan ke `analysis_history.json` dengan thumbnail untuk pelacakan.

## Instalasi

1. Pastikan Python 3.8 atau lebih baru terpasang.
2. Instal seluruh dependensi dari `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   Berkas ini penting agar layanan seperti Streamlit Cloud otomatis memasang paket yang diperlukan (misalnya `matplotlib`).

## Penggunaan CLI

Jalankan analisis dari terminal melalui `main.py`:

```bash
python main.py <path_gambar> [--output-dir DIR] [--export-all|--export-vis|--export-report]
```

Opsi:
- `--output-dir`  Direktori penyimpanan hasil (default `./results`).
- `--export-all`  Membuat paket lengkap (visualisasi PNG, laporan DOCX/PDF, dsb.).
- `--export-vis`  Hanya menyimpan visualisasi.
- `--export-report`  Hanya menyimpan laporan DOCX.

Hasil analisis akan dicatat pada terminal dan ringkasannya otomatis ditambahkan ke `analysis_history.json`.

## Antarmuka Streamlit

Untuk antarmuka grafis berbasis web, jalankan:

```bash
streamlit run app2.py
```

Aplikasi menyediakan tab untuk mengunggah gambar, melihat hasil analisis, mengelola riwayat, serta mengekspor laporan.

## Riwayat & Pengujian

- Berkas `analysis_history.json` menyimpan riwayat analisis lengkap beserta thumbnail (disimpan pada folder `history_thumbnails`).
- Skrip `test_history_util.py` dapat dijalankan untuk menguji fungsi penyimpanan dan pemuatan riwayat:
  ```bash
  python test_history_util.py
  ```

## Contoh Struktur Hasil

Setelah analisis, direktori keluaran berisi berkas seperti:

```
results/
├── <nama_file>_analysis.png      # visualisasi analisis
├── <nama_file>_report.docx       # laporan (opsional)
├── <nama_file>_report.pdf        # laporan PDF (opsional)
└── process_images/               # (jika diekspor penuh) tahapan proses
```

## Kontribusi

Repositori ini belum dilengkapi unit test menyeluruh dan masih dapat dikembangkan lebih lanjut. Silakan ajukan *pull request* atau laporkan isu jika menemukan masalah.


