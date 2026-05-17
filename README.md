# 🎮 Hand Gesture Volume Control

Aplikasi pengolahan citra yang menggunakan **gesture tangan** untuk mengontrol volume sistem secara real-time menggunakan webcam.

---

## 📋 Fitur

- ✅ Deteksi tangan real-time menggunakan MediaPipe
- ✅ Kontrol volume dengan jarak antara jari telunjuk dan ibu jari
- ✅ Indikator visual volume pada layar
- ✅ FPS counter untuk monitoring performa
- ✅ Tersedia versi Windows dan MacOS
- ✅ Gesture validation dengan minggir jari kelingking

---

## 🛠️ Persyaratan Sistem

### Hardware

- **Webcam** yang terhubung dengan komputer
- **Processor** yang mendukung OpenCV (minimum Intel i5 / AMD Ryzen 5)
- **RAM** minimal 4GB

### Software

- **Python 3.7+** (rekomendasi: Python 3.8 - 3.10)
- Sistem operasi: **Windows 10+** atau **MacOS 10.14+**

---

## 📦 Instalasi

### 1. Clone atau Download Project

```bash
cd "Semester 6/Pengolahan Citra/Project Pengolahan Citra"
```

### 2. Buat Virtual Environment (Opsional tapi Disarankan)

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**MacOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Buat file `requirements.txt` dengan konten berikut atau langsung install library-nya:

**Cara 1: Menggunakan requirements.txt**

```bash
pip install -r requirements.txt
```

**Cara 2: Install Satu Per Satu**

#### Untuk Windows:

```bash
pip install opencv-python
pip install mediapipe
pip install numpy
pip install pycaw
pip install comtypes
```

#### Untuk MacOS:

```bash
pip install opencv-python
pip install mediapipe
pip install numpy
```

---

## 📋 Daftar Dependencies

| Library           | Versi      | Fungsi                                     |
| ----------------- | ---------- | ------------------------------------------ |
| **opencv-python** | >=4.5.0    | Pemrosesan citra dan display video         |
| **mediapipe**     | >=0.8.0    | Deteksi dan tracking tangan                |
| **numpy**         | >=1.19.0   | Operasi numerik dan interpolasi            |
| **pycaw**         | >=20230407 | Control volume Windows (Windows only)      |
| **comtypes**      | >=1.1.0    | COM interface untuk Windows (Windows only) |

---

## 🚀 Cara Menjalankan

### Windows

```bash
python "GestureVolumeControl(Windows).py"
```

### MacOS

```bash
python3 "GestureVolumeControl(MacOS).py"
```

---

## 📖 Cara Penggunaan

1. **Buka aplikasi** - Program akan membuka jendela webcam
2. **Tunjukkan tangan** - Posisikan tangan di depan webcam
3. **Kontrol Volume**:
   - Jarak jari telunjuk & ibu jari **minimal** = volume **minimum**
   - Jarak jari telunjuk & ibu jari **maksimal** = volume **maksimal**
   - **Turunkan jari kelingking** = volume mode **AKTIF** (lingkaran hijau)
   - **Naikkan jari kelingking** = volume mode **TIDAK AKTIF** (lingkaran merah)
4. **Keluar** - Tekan tombol **Q** pada keyboard untuk exit

---

## 🎯 Gesture Explanation

### Deteksi Tangan

- Program mendeteksi **21 landmark** pada setiap tangan
- Landmark meliputi: ujung jari, buku jari, dan pergelangan tangan

### Volume Control

```
Posisi Jari Telunjuk & Ibu Jari:
┌─────────────────────────────┐
│ Jauh (50-200 px)            │
│ Min ← Volume → Max          │
│ Dekat                       │
└─────────────────────────────┘
```

### Gesture Aktivasi

- **Pinky Down** (jari kelingking turun) = Volume Control AKTIF
- **Pinky Up** (jari kelingking naik) = Volume Control TIDAK AKTIF

---

## 🔧 Troubleshooting

### Masalah: Webcam tidak terdeteksi

**Solusi:**

- Pastikan webcam terhubung dan tidak digunakan aplikasi lain
- Coba ganti `cv2.VideoCapture(0)` dengan `cv2.VideoCapture(1)` atau nomor lain
- Periksa permission aplikasi di settings sistem

### Masalah: Tangan tidak terdeteksi dengan baik

**Solusi:**

- Pastikan pencahayaan cukup terang
- Ubah parameter `detectionCon` (0.7) menjadi lebih rendah (0.5 atau 0.6)
- Jauhkan tangan dari kamera agar terlihat penuh

### Masalah: Volume tidak berubah (Windows)

**Solusi:**

- Pastikan library `pycaw` dan `comtypes` sudah terinstall
- Jalankan aplikasi dengan hak akses Administrator
- Cek apakah speaker aktif di system audio settings

### Masalah: Volume tidak berubah (MacOS)

**Solusi:**

- Pastikan MacOS mengizinkan Terminal untuk mengontrol volume
- Buka **System Preferences → Security & Privacy → Privacy → Microphone/Audio**
- Tambahkan Terminal ke daftar allowed apps

### Masalah: FPS rendah

**Solusi:**

- Kurangi resolusi webcam (ganti 640x480 dengan 320x240)
- Tutup aplikasi berat lainnya
- Upgrade spesifikasi hardware

---

## 📊 Performa

| Komponen                 | Requirement     |
| ------------------------ | --------------- |
| **Detection Confidence** | 0.7 (70%)       |
| **Max Hands**            | 1 (satu tangan) |
| **Resolution**           | 640x480 px      |
| **Expected FPS**         | 20-30 FPS       |

---

## 📁 Struktur Project

```
Project Pengolahan Citra/
├── GestureVolumeControl(Windows).py    # Versi Windows
├── GestureVolumeControl(MacOS).py      # Versi MacOS
├── requirements.txt                    # Dependencies list
└── README.md                          # File ini
```

---

## 📝 Notes

- **Windows**: Menggunakan `pycaw` library untuk COM interface system audio
- **MacOS**: Menggunakan `osascript` command untuk AppleScript integration
- Program menggunakan **smoothing** agar volume tidak berubah-ubah drastis
- Detection confidence bisa disesuaikan untuk berbagai kondisi lighting

---

## 👨‍💻 Pengembang

Dibuat untuk project **Pengolahan Citra Semester 6**

---

## 📜 License

Free to use for educational purposes

---

## ❓ FAQ

**Q: Bisakah menggunakan kedua tangan?**
A: Tidak, saat ini program hanya support 1 tangan. Untuk support 2 tangan, ubah parameter `maxHands` menjadi 2.

**Q: Bagaimana cara mengubah sensitivitas?**
A: Ubah parameter `detectionCon` dan `trackCon` di class `HandDetector`, atau ubah range `[50, 200]` di fungsi volume mapping.

**Q: Apakah bisa digunakan di Linux?**
A: Versi Linux belum tersedia, tapi bisa dicoba dengan modifikasi untuk command line volume control.

**Q: Apakah perlu koneksi internet?**
A: Tidak, aplikasi bekerja 100% offline setelah install.

---

**🎉 Selamat menggunakan Hand Gesture Volume Control!**

# Gesture_Volume_Control
