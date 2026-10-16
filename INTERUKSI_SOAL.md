# Instruksi Soal: Rekomendasi Produk dengan Machine Learning

## Tujuan

Siapkan proyek klasifikasi untuk membandingkan beberapa algoritma machine learning, lalu gunakan algoritma dengan hasil terbaik pada aplikasi rekomendasi produk. Aplikasi harus membantu mengetahui produk yang direkomendasikan untuk dijual pada bulan Oktober dan tahun data yang menjadi dasar rekomendasi.

## Langkah pengerjaan

1. **Periksa versi Python** yang terpasang:

   ```powershell
   python --version
   ```

   Gunakan Python 3.11 atau versi yang kompatibel dengan dependensi proyek.

2. **Clone proyek** dari repository yang diberikan:

   ```powershell
   git clone <URL_REPOSITORY>
   cd <NAMA_FOLDER_PROYEK>
   ```

   Ganti `<URL_REPOSITORY>` dengan URL repository proyek dan `<NAMA_FOLDER_PROYEK>` dengan folder hasil cloning.

3. **Siapkan environment dan dependensi** proyek. Disarankan menggunakan virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install --upgrade pip
   pip install pandas scikit-learn streamlit
   ```

   Jika PowerShell memblokir aktivasi environment, jalankan:

   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

   Kemudian aktifkan kembali environment.

4. **Atur pembacaan dataset** pada `app.py` dan `comparation.py` agar keduanya membaca file `dataset_penjualan_produk.csv`. Simpan dataset di folder utama proyek atau gunakan path yang sesuai dengan lokasi file tersebut.

5. **Atur pembagian data** pada proses pelatihan di `app.py` dan `comparation.py` menjadi:
   - 70% data training
   - 30% data testing

   Pastikan pembagian dilakukan secara konsisten dan data testing tidak digunakan untuk melatih model.

6. **Bandingkan algoritma** dengan menjalankan:

   ```powershell
   python comparation.py
   ```

   Catat akurasi setiap algoritma. Tentukan algoritma terbaik berdasarkan akurasi pada data testing, lalu catat juga hasil dan alasan pemilihannya.

7. **Gunakan algoritma terbaik** dari hasil perbandingan sebagai model pada `app.py`. Pastikan fitur dan proses encoding yang diperlukan untuk training dan prediksi konsisten.

8. **Jalankan aplikasi**:

   ```powershell
   streamlit run app.py
   ```

   Pada aplikasi, pilih bulan Oktober dan jalankan rekomendasi. Periksa hasil berdasarkan tahun pada dataset, lalu catat tahun dan produk yang direkomendasikan untuk dijual pada bulan Oktober.

## Hasil yang dikumpulkan

- `app.py` dan `comparation.py` yang membaca `dataset_penjualan_produk.csv`.
- Kedua skrip menggunakan pembagian data 70% training dan 30% testing.
- Hasil perbandingan algoritma beserta algoritma terbaik yang dipilih.
- Hasil rekomendasi produk untuk bulan Oktober, termasuk tahun data yang menjadi dasar rekomendasi.

## Catatan evaluasi

Jika aplikasi hanya menyediakan pilihan bulan dan belum menampilkan atau membedakan tahun, sesuaikan aplikasi agar tahun rekomendasi dapat diketahui dari dataset. Jangan menyimpulkan satu tahun tertentu apabila hasil aplikasi belum memberikan informasi tahun yang mendukung kesimpulan tersebut.

