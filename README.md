# Screenshot App dengan Floating Windows

Aplikasi Android untuk mengambil screenshot dengan area kustom menggunakan floating windows.

## Fitur
- Floating windows dengan tombol kontrol
- Overlay canvas untuk menggambar persegi panjang
- Drag & resize rectangle
- Penomoran otomatis (001, 002, dst)
- Double click untuk renumber dan delete
- Screenshot dengan crop sesuai rectangle
- Save gambar dengan format PNG

## Cara Install
1. Buka project di Android Studio
2. Build APK
3. Install di device Android
4. Berikan izin overlay dan storage

## Struktur File
.
├── app/
│   ├── src/main/java/com/example/screenshotapp/
│   │   ├── MainActivity.kt
│   │   ├── FloatingWindowService.kt
│   │   ├── OverlayCanvas.kt
│   │   └── MediaProjectionActivity.kt
│   ├── src/main/res/layout/
│   │   ├── activity_main.xml
│   │   ├── floating_buttons.xml
│   │   ├── overlay_layout.xml
│   │   └── dialog_name.xml
│   └── build.gradle
├── build.gradle
└── settings.gradle
