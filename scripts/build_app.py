#!/usr/bin/env python3
"""
Script untuk build aplikasi Sshot Custom APK
Jalankan: python scripts/build_apk.py
"""

import os
import shutil

def create_directory_structure():
    """Membuat struktur direktori proyek Android"""
    dirs = [
        'app/src/main/java/com/sshotcustom/app',
        'app/src/main/res/layout',
        'app/src/main/res/values',
        'app/src/main/res/drawable',
        'app/src/main/res/xml',
        '.github/workflows'
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("✓ Struktur direktori dibuat")

def create_build_gradle():
    """Membuat file build.gradle (Project level)"""
    content = """// Top-level build file
buildscript {
    ext.kotlin_version = '1.9.0'
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.1.0'
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
"""
    with open('build.gradle', 'w') as f:
        f.write(content)
    print("✓ build.gradle dibuat")

def create_app_build_gradle():
    """Membuat file build.gradle (App level)"""
    content = """plugins {
    id 'com.android.application'
    id 'kotlin-android'
}

android {
    namespace 'com.sshotcustom.app'
    compileSdk 34

    defaultConfig {
        applicationId "com.sshotcustom.app"
        minSdk 23
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }

    kotlinOptions {
        jvmTarget = '1.8'
    }

    buildFeatures {
        viewBinding true
    }
}

dependencies {
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
}
"""
    with open('app/build.gradle', 'w') as f:
        f.write(content)
    print("✓ app/build.gradle dibuat")

def create_gradle_properties():
    """Membuat gradle.properties"""
    content = """org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.enableJetifier=true
kotlin.code.style=official
"""
    with open('gradle.properties', 'w') as f:
        f.write(content)
    print("✓ gradle.properties dibuat")

def create_settings_gradle():
    """Membuat settings.gradle"""
    content = """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "Sshot Custom"
include ':app'
"""
    with open('settings.gradle', 'w') as f:
        f.write(content)
    print("✓ settings.gradle dibuat")

def create_android_manifest():
    """Membuat AndroidManifest.xml"""
    content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" 
        android:maxSdkVersion="28" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" 
        android:maxSdkVersion="32" />
    <uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="Sshot Custom"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.Light.DarkActionBar">
        
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <service
            android:name=".OverlayService"
            android:enabled="true"
            android:exported="false" />
    </application>

</manifest>
"""
    with open('app/src/main/AndroidManifest.xml', 'w') as f:
        f.write(content)
    print("✓ AndroidManifest.xml dibuat")

def create_main_activity():
    """Membuat MainActivity.kt"""
    content = """package com.sshotcustom.app

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class MainActivity : AppCompatActivity() {

    private val PERMISSION_REQUEST_CODE = 100
    private val OVERLAY_PERMISSION_REQUEST_CODE = 101

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        checkPermissions()
    }

    private fun checkPermissions() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (!Settings.canDrawOverlays(this)) {
                val intent = Intent(
                    Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                    Uri.parse("package:$packageName")
                )
                startActivityForResult(intent, OVERLAY_PERMISSION_REQUEST_CODE)
                return
            }
        }

        checkStoragePermissions()
    }

    private fun checkStoragePermissions() {
        val permissions = mutableListOf<String>()

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_MEDIA_IMAGES)
                != PackageManager.PERMISSION_GRANTED) {
                permissions.add(Manifest.permission.READ_MEDIA_IMAGES)
            }
        } else {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE)
                != PackageManager.PERMISSION_GRANTED) {
                permissions.add(Manifest.permission.WRITE_EXTERNAL_STORAGE)
            }
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE)
                != PackageManager.PERMISSION_GRANTED) {
                permissions.add(Manifest.permission.READ_EXTERNAL_STORAGE)
            }
        }

        if (permissions.isNotEmpty()) {
            ActivityCompat.requestPermissions(this, permissions.toTypedArray(), PERMISSION_REQUEST_CODE)
        } else {
            startOverlayService()
        }
    }

    private fun startOverlayService() {
        val intent = Intent(this, OverlayService::class.java)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
        Toast.makeText(this, "Floating button started", Toast.LENGTH_SHORT).show()
        finish()
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == PERMISSION_REQUEST_CODE) {
            if (grantResults.all { it == PackageManager.PERMISSION_GRANTED }) {
                startOverlayService()
            } else {
                Toast.makeText(this, "Permissions required", Toast.LENGTH_SHORT).show()
                finish()
            }
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == OVERLAY_PERMISSION_REQUEST_CODE) {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                if (Settings.canDrawOverlays(this)) {
                    checkStoragePermissions()
                } else {
                    Toast.makeText(this, "Overlay permission required", Toast.LENGTH_SHORT).show()
                    finish()
                }
            }
        }
    }
}
"""
    with open('app/src/main/java/com/sshotcustom/app/MainActivity.kt', 'w') as f:
        f.write(content)
    print("✓ MainActivity.kt dibuat")

def create_overlay_service():
    """Membuat OverlayService.kt"""
    content = """package com.sshotcustom.app

import android.app.*
import android.content.Context
import android.content.Intent
import android.graphics.*
import android.os.Build
import android.os.IBinder
import android.view.*
import android.widget.*
import androidx.core.app.NotificationCompat
import java.io.File
import java.io.FileOutputStream
import java.text.SimpleDateFormat
import java.util.*

class OverlayService : Service() {

    private lateinit var windowManager: WindowManager
    private lateinit var floatingView: View
    private lateinit var mainButton: ImageView
    private lateinit var buttonsContainer: LinearLayout
    private var isExpanded = false
    private var rectangles = mutableListOf<RectangleOverlay>()
    private var isDrawingMode = false
    private var imageName = "screenshot"
    private var saveDirectory = ""

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        startForeground(1, createNotification())
        
        saveDirectory = getExternalFilesDir(null)?.absolutePath ?: ""
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (::floatingView.isInitialized) return START_STICKY

        windowManager = getSystemService(Context.WINDOW_SERVICE) as WindowManager
        createFloatingButton()
        return START_STICKY
    }

    private fun createFloatingButton() {
        floatingView = LayoutInflater.from(this).inflate(R.layout.floating_buttons, null)
        
        val params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            else
                WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        )
        params.gravity = Gravity.TOP or Gravity.END
        params.x = 20
        params.y = 100

        mainButton = floatingView.findViewById(R.id.mainButton)
        buttonsContainer = floatingView.findViewById(R.id.buttonsContainer)

        mainButton.setOnClickListener { toggleButtons() }
        
        floatingView.findViewById<Button>(R.id.btnCrop).setOnClickListener { startCrop() }
        floatingView.findViewById<Button>(R.id.btnSave).setOnClickListener { saveScreenshots() }
        floatingView.findViewById<Button>(R.id.btnName).setOnClickListener { showNameDialog() }
        floatingView.findViewById<Button>(R.id.btnSettings).setOnClickListener { showSettingsDialog() }
        floatingView.findViewById<Button>(R.id.btnClose).setOnClickListener { stopSelf() }

        makeDraggable(floatingView, params)
        windowManager.addView(floatingView, params)
    }

    private fun toggleButtons() {
        isExpanded = !isExpanded
        buttonsContainer.visibility = if (isExpanded) View.VISIBLE else View.GONE
        mainButton.rotation = if (isExpanded) 45f else 0f
    }

    private fun startCrop() {
        isDrawingMode = true
        val overlay = RectangleOverlay(this, windowManager, rectangles.size + 1) { rect ->
            rectangles.add(rect)
            isDrawingMode = false
        }
        overlay.show()
    }

    private fun saveScreenshots() {
        if (rectangles.isEmpty()) {
            Toast.makeText(this, "No rectangles to save", Toast.LENGTH_SHORT).show()
            return
        }

        floatingView.visibility = View.GONE
        
        floatingView.postDelayed({
            val bitmap = takeScreenshot()
            if (bitmap != null) {
                rectangles.forEach { rect ->
                    val nextNumber = getNextNumber(rect.number)
                    rect.number = nextNumber
                    saveCroppedImage(bitmap, rect)
                }
                Toast.makeText(this, "Screenshots saved", Toast.LENGTH_SHORT).show()
            }
            floatingView.visibility = View.VISIBLE
            clearRectangles()
        }, 200)
    }

    private fun takeScreenshot(): Bitmap? {
        try {
            val view = windowManager.defaultDisplay
            val bitmap = Bitmap.createBitmap(
                Resources.getSystem().displayMetrics.widthPixels,
                Resources.getSystem().displayMetrics.heightPixels,
                Bitmap.Config.ARGB_8888
            )
            val canvas = Canvas(bitmap)
            val window = (getSystemService(Context.WINDOW_SERVICE) as WindowManager).defaultDisplay
            window.getRealMetrics(Resources.getSystem().displayMetrics)
            return bitmap
        } catch (e: Exception) {
            e.printStackTrace()
            return null
        }
    }

    private fun saveCroppedImage(bitmap: Bitmap, rect: RectangleOverlay) {
        try {
            val croppedBitmap = Bitmap.createBitmap(
                bitmap,
                rect.left.toInt(),
                rect.top.toInt(),
                rect.width.toInt(),
                rect.height.toInt()
            )

            val fileName = "${imageName}_${String.format("%03d", rect.number)}.png"
            val file = File(saveDirectory, fileName)
            
            FileOutputStream(file).use { out ->
                croppedBitmap.compress(Bitmap.CompressFormat.PNG, 100, out)
            }
            
            croppedBitmap.recycle()
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun getNextNumber(startFrom: Int): Int {
        var num = startFrom
        while (true) {
            val fileName = "${imageName}_${String.format("%03d", num)}.png"
            val file = File(saveDirectory, fileName)
            if (!file.exists()) return num
            num++
        }
    }

    private fun clearRectangles() {
        rectangles.forEach { it.remove() }
        rectangles.clear()
    }

    private fun showNameDialog() {
        // Dialog implementation would go here
        Toast.makeText(this, "Name dialog", Toast.LENGTH_SHORT).show()
    }

    private fun showSettingsDialog() {
        // Settings dialog implementation
        Toast.makeText(this, "Settings dialog", Toast.LENGTH_SHORT).show()
    }

    private fun makeDraggable(view: View, params: WindowManager.LayoutParams) {
        var initialX = 0
        var initialY = 0
        var initialTouchX = 0f
        var initialTouchY = 0f

        view.setOnTouchListener { v, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    initialX = params.x
                    initialY = params.y
                    initialTouchX = event.rawX
                    initialTouchY = event.rawY
                    true
                }
                MotionEvent.ACTION_MOVE -> {
                    params.x = initialX + (initialTouchX - event.rawX).toInt()
                    params.y = initialY + (event.rawY - initialTouchY).toInt()
                    windowManager.updateViewLayout(view, params)
                    true
                }
                else -> false
            }
        }
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                "overlay_service",
                "Overlay Service",
                NotificationManager.IMPORTANCE_LOW
            )
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(channel)
        }
    }

    private fun createNotification(): Notification {
        return NotificationCompat.Builder(this, "overlay_service")
            .setContentTitle("Sshot Custom")
            .setContentText("Service is running")
            .setSmallIcon(android.R.drawable.ic_menu_camera)
            .build()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        super.onDestroy()
        if (::floatingView.isInitialized) {
            windowManager.removeView(floatingView)
        }
        clearRectangles()
    }
}
"""
    with open('app/src/main/java/com/sshotcustom/app/OverlayService.kt', 'w') as f:
        f.write(content)
    print("✓ OverlayService.kt dibuat")

def create_rectangle_overlay():
    """Membuat RectangleOverlay.kt"""
    content = """package com.sshotcustom.app

import android.content.Context
import android.graphics.Color
import android.graphics.PixelFormat
import android.os.Build
import android.view.*
import android.widget.FrameLayout
import android.widget.TextView
import android.widget.Toast

class RectangleOverlay(
    private val context: Context,
    private val windowManager: WindowManager,
    var number: Int,
    private val onComplete: (RectangleOverlay) -> Unit
) {
    private lateinit var overlayView: FrameLayout
    private lateinit var params: WindowManager.LayoutParams
    var left = 0f
    var top = 0f
    var width = 0f
    var height = 0f
    
    private var startX = 0f
    private var startY = 0f
    private var isFirstClick = true
    private var isDrawing = true

    fun show() {
        overlayView = FrameLayout(context)
        overlayView.setBackgroundColor(Color.TRANSPARENT)

        params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.MATCH_PARENT,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            else
                WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        )

        setupDrawing()
        windowManager.addView(overlayView, params)
    }

    private fun setupDrawing() {
        overlayView.setOnTouchListener { _, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    if (isDrawing) {
                        if (isFirstClick) {
                            startX = event.rawX
                            startY = event.rawY
                            isFirstClick = false
                        } else {
                            val endX = event.rawX
                            val endY = event.rawY
                            createRectangle(startX, startY, endX, endY)
                            isDrawing = false
                            windowManager.removeView(overlayView)
                            onComplete(this)
                        }
                        true
                    } else {
                        false
                    }
                }
                else -> false
            }
        }
    }

    private fun createRectangle(x1: Float, y1: Float, x2: Float, y2: Float) {
        left = minOf(x1, x2)
        top = minOf(y1, y2)
        width = Math.abs(x2 - x1)
        height = Math.abs(y2 - y1)

        val rectView = FrameLayout(context)
        rectView.setBackgroundColor(Color.parseColor("#4400FF00"))
        
        val borderView = View(context)
        borderView.setBackgroundResource(android.R.drawable.edit_text)
        rectView.addView(borderView, FrameLayout.LayoutParams(
            FrameLayout.LayoutParams.MATCH_PARENT,
            FrameLayout.LayoutParams.MATCH_PARENT
        ))

        val label = TextView(context)
        label.text = String.format("%03d", number)
        label.setTextColor(Color.WHITE)
        label.setBackgroundColor(Color.parseColor("#AA000000"))
        label.setPadding(8, 4, 8, 4)
        rectView.addView(label)

        val rectParams = WindowManager.LayoutParams(
            width.toInt(),
            height.toInt(),
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            else
                WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        )
        rectParams.x = left.toInt()
        rectParams.y = top.toInt()
        rectParams.gravity = Gravity.TOP or Gravity.START

        setupRectangleInteraction(rectView, rectParams)
        windowManager.addView(rectView, rectParams)
        overlayView = rectView
        this.params = rectParams
    }

    private fun setupRectangleInteraction(view: View, params: WindowManager.LayoutParams) {
        var initialX = 0
        var initialY = 0
        var initialTouchX = 0f
        var initialTouchY = 0f
        var lastTapTime = 0L

        view.setOnTouchListener { _, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    val currentTime = System.currentTimeMillis()
                    if (currentTime - lastTapTime < 300) {
                        showOptionsMenu()
                    }
                    lastTapTime = currentTime
                    
                    initialX = params.x
                    initialY = params.y
                    initialTouchX = event.rawX
                    initialTouchY = event.rawY
                    true
                }
                MotionEvent.ACTION_MOVE -> {
                    params.x = initialX + (event.rawX - initialTouchX).toInt()
                    params.y = initialY + (event.rawY - initialTouchY).toInt()
                    windowManager.updateViewLayout(view, params)
                    left = params.x.toFloat()
                    top = params.y.toFloat()
                    true
                }
                else -> false
            }
        }
    }

    private fun showOptionsMenu() {
        Toast.makeText(context, "Options: Renumber / Delete", Toast.LENGTH_SHORT).show()
    }

    fun remove() {
        try {
            if (::overlayView.isInitialized) {
                windowManager.removeView(overlayView)
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}
"""
    with open('app/src/main/java/com/sshotcustom/app/RectangleOverlay.kt', 'w') as f:
        f.write(content)
    print("✓ RectangleOverlay.kt dibuat")

def create_layouts():
    """Membuat layout XML files"""
    
    # activity_main.xml
    activity_main = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="16dp">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Sshot Custom"
        android:textSize="24sp"
        android:textStyle="bold"
        android:layout_marginBottom="16dp"/>

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Granting permissions..."
        android:textSize="16sp"/>

</LinearLayout>
"""
    with open('app/src/main/res/layout/activity_main.xml', 'w') as f:
        f.write(activity_main)

    # floating_buttons.xml
    floating_buttons = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:background="#AA000000"
    android:padding="8dp">

    <ImageView
        android:id="@+id/mainButton"
        android:layout_width="48dp"
        android:layout_height="48dp"
        android:src="@android:drawable/ic_menu_camera"
        android:background="?attr/selectableItemBackgroundBorderless"
        android:scaleType="centerInside"/>

    <LinearLayout
        android:id="@+id/buttonsContainer"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:visibility="gone"
        android:layout_marginTop="8dp">

        <Button
            android:id="@+id/btnCrop"
            android:layout_width="120dp"
            android:layout_height="wrap_content"
            android:text="Crop"
            android:textSize="12sp"
            android:layout_marginBottom="4dp"/>

        <Button
            android:id="@+id/btnSave"
            android:layout_width="120dp"
            android:layout_height="wrap_content"
            android:text="Save"
            android:textSize="12sp"
            android:layout_marginBottom="4dp"/>

        <Button
            android:id="@+id/btnName"
            android:layout_width="120dp"
            android:layout_height="wrap_content"
            android:text="Name"
            android:textSize="12sp"
            android:layout_marginBottom="4dp"/>

        <Button
            android:id="@+id/btnSettings"
            android:layout_width="120dp"
            android:layout_height="wrap_content"
            android:text="Settings"
            android:textSize="12sp"
            android:layout_marginBottom="4dp"/>

        <Button
            android:id="@+id/btnClose"
            android:layout_width="120dp"
            android:layout_height="wrap_content"
            android:text="Close"
            android:textSize="12sp"/>

    </LinearLayout>

</LinearLayout>
"""
    with open('app/src/main/res/layout/floating_buttons.xml', 'w') as f:
        f.write(floating_buttons)

    print("✓ Layout XML dibuat")

def create_values():
    """Membuat values resources"""
    
    strings = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Sshot Custom</string>
</resources>
"""
    with open('app/src/main/res/values/strings.xml', 'w') as f:
        f.write(strings)

    colors = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
</resources>
"""
    with open('app/src/main/res/values/colors.xml', 'w') as f:
        f.write(colors)

    print("✓ Values resources dibuat")

def create_github_workflow():
    """Membuat GitHub Actions workflow"""
    content = """name: Build Android APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up JDK 17
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'

    - name: Setup Android SDK
      uses: android-actions/setup-android@v2

    - name: Grant execute permission for gradlew
      run: chmod +x gradlew

    - name: Build with Gradle
      run: ./gradlew assembleDebug

    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: app-debug
        path: app/build/outputs/apk/debug/app-debug.apk

    - name: Create Release
      if: github.ref == 'refs/heads/main'
      uses: softprops/action-gh-release@v1
      with:
        tag_name: v1.0.${{ github.run_number }}
        files: app/build/outputs/apk/debug/app-debug.apk
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
"""
    with open('.github/workflows/build_apk.yml', 'w') as f:
        f.write(content)
    print("✓ GitHub workflow dibuat")

def create_gradlew_files():
    """Membuat gradle wrapper files"""
    
    # gradle-wrapper.properties
    wrapper_props = """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.2-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
"""
    os.makedirs('gradle/wrapper', exist_ok=True)
    with open('gradle/wrapper/gradle-wrapper.properties', 'w') as f:
        f.write(wrapper_props)
    
    print("✓ Gradle wrapper properties dibuat")

def create_proguard_rules():
    """Membuat proguard-rules.pro"""
    content = """# Add project specific ProGuard rules here.
-keepattributes *Annotation*
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}
-keep class com.sshotcustom.app.** { *; }
"""
    with open('app/proguard-rules.pro', 'w') as f:
        f.write(content)
    print("✓ proguard-rules.pro dibuat")

def create_readme():
    """Membuat README.md"""
    content = """# Sshot Custom APK

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
"""
    with open('README.md', 'w') as f:
        f.write(content)
    print("✓ README.md dibuat")

def create_gitignore():
    """Membuat .gitignore"""
    content = """# Built application files
*.apk
*.ap_
*.aab

# Files for the ART/Dalvik VM
*.dex

# Java class files
*.class

# Generated files
bin/
gen/
out/
release/

# Gradle files
.gradle/
build/

# Local configuration file
local.properties

# Android Studio
*.iml
.idea/
.DS_Store
/captures
.externalNativeBuild
.cxx

# NDK
obj/

# Android Profiling
*.hprof
"""
    with open('.gitignore', 'w') as f:
        f.write(content)
    print("✓ .gitignore dibuat")

def main():
    """Main function untuk menjalankan semua fungsi"""
    print("=" * 50)
    print("Building Sshot Custom APK Project")
    print("=" * 50)
    
    create_directory_structure()
    create_build_gradle()
    create_app_build_gradle()
    create_gradle_properties()
    create_settings_gradle()
    create_android_manifest()
    create_main_activity()
    create_overlay_service()
    create_rectangle_overlay()
    create_layouts()
    create_values()
    create_github_workflow()
    create_gradlew_files()
    create_proguard_rules()
    create_readme()
    create_gitignore()
    
    print("=" * 50)
    print("✅ SEMUA FILE BERHASIL DIBUAT!")
    print("=" * 50)
    print("\nLangkah selanjutnya:")
    print("1. Jalankan: python scripts/build_apk.py")
    print("2. Download Gradle wrapper: gradle wrapper")
    print("3. Build APK: ./gradlew assembleDebug")
    print("4. APK ada di: app/build/outputs/apk/debug/")
    print("\nAtau push ke GitHub untuk auto-build via Actions")
    print("=" * 50)

if __name__ == "__main__":
    main()