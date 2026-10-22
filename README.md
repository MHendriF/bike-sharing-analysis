# 🚲 Proyek Analisis Data: Bike Sharing Dataset

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bike-sharing-analysis-mvm6fzzzczxwfozqjnukur.streamlit.app/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MHendriF/bike-sharing-analysis/blob/main/notebook.ipynb)
![Python Version](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Proyek analisis data eksploratif (EDA) dan visualisasi interaktif menggunakan **Bike Sharing Dataset** dari sistem Capital Bikeshare (Washington D.C., USA) untuk periode tahun 2011 hingga 2012. Proyek ini mencakup proses *Data Wrangling*, *Exploratory Data Analysis*, pembuatan visualisasi analitik, perumusan kesimpulan bisnis, serta penerapan dashboard interaktif berbasis **Streamlit**.

---

## 📌 Daftar Isi
1. [Latar Belakang & Ringkasan Proyek](#-latar-belakang--ringkasan-proyek)
2. [Pertanyaan Bisnis](#-pertanyaan-bisnis)
3. [Temuan Utama & Insight Bisnis](#-temuan-utama--insight-bisnis)
4. [Rekomendasi Strategis](#-rekomendasi-strategis)
5. [Struktur Direktori](#-struktur-direktori)
6. [Deskripsi & Skema Dataset](#-deskripsi--skema-dataset)
7. [Panduan Instalasi & Menjalankan Dashboard](#-panduan-instalasi--menjalankan-dashboard)
8. [Best Practice & Refactoring yang Diterapkan](#-best-practice--refactoring-yang-diterapkan)
9. [Tautan Demo & Repositori](#-tautan-demo--repositori)
10. [Penulis & Atribusi](#-penulis--atribusi)

---

## 📖 Latar Belakang & Ringkasan Proyek

Sistem penyewaan sepeda (*bike sharing*) telah menjadi infrastruktur transportasi penting di berbagai kota modern karena perannya dalam mengurangi kemacetan, menekan jejak karbon, dan mendorong gaya hidup sehat. Berbeda dari transportasi konvensional, sistem penyewaan sepeda mencatat waktu peminjaman, durasi perjalanan, serta stasiun asal-tujuan secara eksplisit. Karakteristik ini membuat data penyewaan sepeda sangat berkorelasi dengan faktor lingkungan, perubahan cuaca, musim, dan rutinitas harian warga.

Tujuan utama dari proyek ini adalah mengeksplorasi faktor-faktor yang mendorong tingkat permintaan (*rental demand*), mengidentifikasi pola jam sibuk (*commuter traffic*), serta menganalisis segmentasi pelanggan (*registered vs casual users*) sebagai dasar pengambilan keputusan operasional.

---

## ❓ Pertanyaan Bisnis

Proyek ini dirancang untuk menjawab 5 pertanyaan bisnis utama:

1. **Tren Musiman:** Bagaimana tren penyewaan sepeda di tiap musim (*Spring, Summer, Fall, Winter*) pada tahun 2011 dan 2012?
2. **Kondisi Cuaca:** Bagaimana pengaruh situasi cuaca (*good, moderate, bad, worse*) terhadap jumlah pengguna sepeda di tahun 2011 dan 2012?
3. **Pola Bulanan:** Bagaimana perbandingan fluktuasi jumlah penyewaan sepeda setiap bulannya pada tahun 2011 dibandingkan 2012?
4. **Traffic & Jam Operasional:** Kapan jam dengan tingkat penyewaan tertinggi (*peak hours*) dan terendah (*off-peak hours*) dalam sehari?
5. **Segmentasi Pengguna:** Bagaimana komposisi perbandingan antara penyewa kasual (*casual users*) dan penyewa terdaftar (*registered users*)?

---

## 💡 Temuan Utama & Insight Bisnis

Berdasarkan analisis terhadap 17.379 rekaman data operasional per jam:

| Aspek Analisis | Temuan Kunci | Angka / Metrik Signifikan |
| :--- | :--- | :--- |
| **Musim (Season)** | **Musim Gugur (Fall)** adalah periode dengan penyewaan tertinggi selama 2 tahun berturut-turut. Musim Semi (*Spring*) memiliki volume terendah. | Puncak Fall 2012: **641.479** rides (naik signifikan dari 419.650 pada 2011). Spring 2011 terendah: **150.000** rides. |
| **Cuaca (Weather)** | Mayoritas aktivitas terjadi saat cuaca **cerah / sedikit berawan (good)**. Permintaan anjlok drastis saat cuaca buruk (*bad/worse*). | Cuaca cerah 2012: **1.463.120** rides vs Cuaca ekstrem 2012: hanya **187** rides. |
| **Tren Bulanan** | Tahun 2012 menunjukkan pertumbuhan konsisten sepanjang tahun dengan durasi periode ramai yang lebih panjang dibanding 2011. | Puncak 2011 terjadi di **Juni** (143.512), sedangkan puncak 2012 bergeser ke **September** (218.573). |
| **Pola Jam (Hourly Traffic)** | Teridentifikasi pola komuter (*work commuter behavior*) yang sangat kuat, dengan lonjakan tajam pada jam berangkat dan pulang kerja. | Jam puncak: **08:00 AM** dan **05:00 - 06:00 PM** (maksimum 336.860 rides). Titik terendah: **04:00 AM** (4.428 rides). |
| **Segmentasi Pengguna** | Basis pengguna didominasi secara mutlak oleh pelanggan terdaftar (*registered users*). | **81,2% Registered** (2.672.662 rides) vs **18,8% Casual** (620.017 rides). |

---

## 🎯 Rekomendasi Strategis

1. **Optimalisasi Kapasitas Armada Berdasarkan Jam Sibuk:**
   - Menyiapkan distribusi unit dan ketersediaan slot stasiun di area perkantoran pada rentang **07:30 - 09:00 AM** dan **05:00 - 06:30 PM**.
   - Melakukan perawatan dan re-balancing armada pada jam lengang (**01:00 AM - 05:00 AM**).
2. **Mitigasi Penurunan Musim Semi & Cuaca Ekstrem:**
   - Merancang promosi atau tarif musiman pada awal musim semi (*Spring pass*) untuk mengantisipasi volume yang cenderung lambat di kuartal pertama.
   - Mengintegrasikan sistem aplikasi dengan prakiraan cuaca instan (*weather alert*) dan menawarkan diskon proteksi hujan.
3. **Konversi Pengguna Kasual Menjadi Member Berlangganan:**
   - Pengguna kasual menyumbang ~19% dari total penyewaan, mayoritas di akhir pekan dan musim liburan. Berikan penawaran diskon langganan bulanan setelah perjalanan ke-3 untuk meningkatkan *Customer Lifetime Value* (CLV).

---

## 📂 Struktur Direktori

```text
bike-sharing-analysis/
│
├── .devcontainer/             # Konfigurasi container development (VS Code / Codespaces)
│   └── devcontainer.json
│
├── assets/                    # Asset visual (logo, ilustrasi)
│   └── bycicle.png
│
├── dashboard/                 # Kode sumber dashboard interaktif
│   ├── dashboard.py           # Aplikasi Streamlit (terstruktur & modular)
│   └── main_data.csv          # Dataset yang telah dibersihkan & diproses
│
├── data/                      # Dataset mentah & dokumentasi sumber
│   ├── Readme.txt             # Dokumentasi asli dari UCI / Capital Bikeshare
│   ├── day.csv                # Rekaman agregat harian (731 baris)
│   └── hour.csv               # Rekaman detail per jam (17.379 baris)
│
├── notebook.ipynb             # Jupyter Notebook lengkap (Wrangling, EDA, Visualisasi)
├── requirements.txt           # Daftar pustaka Python yang dibutuhkan
├── url.txt                    # Tautan aplikasi dashboard yang aktif (live)
└── README.md                  # Dokumentasi komprehensif proyek
```

---

## 📊 Deskripsi & Skema Dataset

Dataset yang digunakan bersumber dari **Capital Bikeshare System** (Washington D.C.) yang dikompilasi oleh Hadi Fanaee-T (LIAAD, University of Porto).

### Variabel Utama pada `main_data.csv`:
- `date` : Tanggal pencatatan data (`YYYY-MM-DD`).
- `season` : Musim (`Spring`, `Summer`, `Fall`, `Winter`).
- `year` : Tahun (`2011`, `2012`).
- `month` : Bulan (`Jan` hingga `Dec`).
- `hour` : Format jam 12-jam (`12 am` hingga `11 pm`).
- `is_holiday` : Status hari libur nasional (`0` = Tidak, `1` = Ya).
- `weekday` : Hari dalam seminggu (`Sunday` hingga `Saturday`).
- `is_working_day` : Hari kerja aktif (`0` = Akhir pekan/libur, `1` = Hari kerja).
- `weather_situation` : Kondisi cuaca:
  - `good` : Cerah, sedikit berawan, berawan sebagian.
  - `moderate` : Berkabut, berawan tebal, mendung.
  - `bad` : Hujan rintik-rintik, salju ringan, badai petir lokal.
  - `worse` : Hujan lebat, badai es, kabut tebal, salju lebat.
- `temperature` : Temperatur ternormalisasi dalam skala Celsius.
- `feels_like_temperature` : Temperatur semu (*feeling temperature*) ternormalisasi.
- `humidity` : Kelembapan udara ternormalisasi.
- `windspeed` : Kecepatan angin ternormalisasi.
- `casual_users` : Jumlah penyewaan oleh pengguna tidak terdaftar / kasual.
- `registered_users` : Jumlah penyewaan oleh pengguna terdaftar / member.
- `total_users` : Total keseluruhan penyewaan (`casual_users + registered_users`).

---

## 🚀 Panduan Instalasi & Menjalankan Dashboard

### 1. Prasyarat Sistem
- Python versi **3.9** atau lebih baru (disarankan Python 3.10, 3.11, atau 3.12).
- Git (opsional, untuk melakukan clone repositori).

### 2. Kloning Repositori
```bash
git clone https://github.com/MHendriF/bike-sharing-analysis.git
cd bike-sharing-analysis
```

### 3. Buat dan Aktifkan Virtual Environment (Disarankan)

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
.\venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instal Dependensi
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Menjalankan Dashboard Streamlit
Jalankan perintah berikut dari direktori root proyek:
```bash
streamlit run dashboard/dashboard.py
```

Setelah perintah dieksekusi, browser akan otomatis terbuka di alamat:
```text
http://localhost:8501
```

---

## 🛠️ Best Practice & Refactoring yang Diterapkan

Kode pada `dashboard/dashboard.py` dan konfigurasi dependensi telah dimutakhirkan mengikuti standar *software engineering* & *clean code*:

1. **Caching & Efisiensi Data (`@st.cache_data`):**
   - Data `main_data.csv` dimuat menggunakan dekorator `@st.cache_data`. Parsing CSV tidak diulang setiap kali pengguna berinteraksi dengan widget sidebar.
2. **Pemuatan Berkas Aman (*Fallback Mechanism*):**
   - Mengutamakan pembacaan berkas lokal (`Path(__file__).parent / "main_data.csv"` dan logo `assets/bycicle.png`). Jika dijalankan di lingkungan remote/cloud tanpa repositori lokal penuh, script secara otomatis beralih (*graceful fallback*) ke URL mentah GitHub.
3. **Pencegahan Bug Unpacking Date Range pada Streamlit:**
   - Menangani kondisi transisi saat pengguna baru mengklik tanggal awal dan belum memilih tanggal akhir (mencegah error bawaan Streamlit `ValueError: not enough values to unpack`).
4. **Manajemen Memori Visualisasi:**
   - Setiap figure Matplotlib ditutup menggunakan `plt.close(fig)` setelah ditampilkan melalui `st.pyplot(fig)` untuk mencegah *memory leak* pada server Streamlit.
5. **Navigasi Berstruktur (*Tabbed Layout*):**
   - Antarmuka disusun rapi ke dalam 5 tab tematik:
     - 📅 *Tren Musiman & Bulanan*
     - ⛅ *Kondisi Cuaca*
     - ⏰ *Jam Sibuk (Hourly Traffic)*
     - 👥 *Komposisi Pengguna*
     - 📑 *Eksplorasi Data Mentah (dengan opsi ekspor CSV)*
6. **Kerapian Format Angka & Palet Warna:**
   - Angka KPI diformat dengan pemisah ribuan (`f"{val:,}"`).
   - Warna grafik menggunakan palet visual yang ramah pembaca (*Crest, Viridis, Magma*) dengan kontras yang teruji.
7. **Standar Kode PEP 8 & Modularitas:**
   - Menambahkan *type hints* (`pd.DataFrame`, `pd.Series`, `Tuple`), *docstrings* berstandar Google/Sphinx, serta blok eksekusi `if __name__ == "__main__": main()`.

---

## 🌐 Tautan Demo & Repositori

- **Live Streamlit Dashboard:** [https://bike-sharing-analysis-mvm6fzzzczxwfozqjnukur.streamlit.app/](https://bike-sharing-analysis-mvm6fzzzczxwfozqjnukur.streamlit.app/)
- **Notebook Google Colab:** [notebook.ipynb](https://colab.research.google.com/github/MHendriF/bike-sharing-analysis/blob/main/notebook.ipynb)
- **GitHub Repository:** [https://github.com/MHendriF/bike-sharing-analysis](https://github.com/MHendriF/bike-sharing-analysis)

---

## 👤 Penulis & Atribusi

- **Penulis:** Muhamad Hendri Febriansyah
- **Program:** Proyek Analisis Data (Dicoding Academy)
- **Sumber Data:** Fanaee-T, Hadi, and Gama, Joao, *"Event labeling combining ensemble detectors and background knowledge"*, Progress in Artificial Intelligence (2014): pp. 1-15, Springer Berlin Heidelberg. [Capital Bikeshare Data](https://www.capitalbikeshare.com/system-data).