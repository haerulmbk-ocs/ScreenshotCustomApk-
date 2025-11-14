# Sshot Custom APK

Aplikasi Android untuk screenshot custom dengan fitur crop persegi panjang.

## Fitur
- Tombol floating untuk kontrol aplikasi
- Membuat persegi panjang custom untuk crop
- Penomoran otomatis screenshot
- Pengaturan nama file output
- Pengaturan direktori penyimpanan

## Build Instructions

### Local Build
```bash
python scripts/build_apk.py
./gradlew assembleDebug
```

APK akan tersedia di: `app/build/outputs/apk/debug/app-debug.apk`

### GitHub Actions Build
1. Push code ke repository GitHub
2. GitHub Actions akan otomatis build APK
3. Download APK dari Artifacts

## Permissions Required
- SYSTEM_ALERT_WINDOW - Untuk floating overlay
- WRITE_EXTERNAL_STORAGE - Menyimpan screenshot (Android <= 10)
- READ_MEDIA_IMAGES - Akses media (Android >= 13)

## Cara Penggunaan
1. Buka aplikasi dan berikan permissions
2. Klik tombol floating utama untuk expand menu
3. Klik "Crop" untuk mulai membuat persegi panjang
4. Klik 2 titik untuk membentuk persegi panjang
5. Klik "Save" untuk menyimpan screenshot
6. File disimpan dengan format: `{nama}_{nomor}.png`

## Struktur Project
```
├── app/
│   ├── src/main/
│   │   ├── java/com/sshotcustom/app/
│   │   │   ├── MainActivity.kt
│   │   │   ├── OverlayService.kt
│   │   │   └── RectangleOverlay.kt
│   │   ├── res/
│   │   │   ├── layout/
│   │   │   └── values/
│   │   └── AndroidManifest.xml
│   └── build.gradle
├── gradle/
├── scripts/
│   └── build_apk.py
├── .github/workflows/
│   └── build_apk.yml
└── build.gradle
```

## License
MIT License
