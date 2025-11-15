import os
import shutil

def create_screenshot_app():
    print("🚀 Membuat project Android Screenshot App...")
    
    # Hapus file dan folder lama jika ada
    files_to_remove = ['gradlew', 'gradlew.bat', 'build.gradle', 'settings.gradle', 'gradle.properties']
    folders_to_remove = ['app', 'gradle', 'build']
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ Menghapus file: {file}")
    
    for folder in folders_to_remove:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"🗑️ Menghapus folder: {folder}")
    
    # Struktur direktori lengkap
    directories = [
        'app/src/main/java/com/example/screenshotapp',
        'app/src/main/res/layout',
        'app/src/main/res/values',
        'app/src/main/res/drawable',
        'gradle/wrapper'
    ]
    
    # Buat semua direktori
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Buat semua file dengan versi yang diperbarui
    create_gradle_properties()
    create_main_activity()
    create_floating_window_service()
    create_overlay_canvas()
    create_media_projection_activity()
    create_activity_main_xml()
    create_floating_buttons_xml()
    create_overlay_layout_xml()
    create_dialog_name_xml()
    create_android_manifest()
    create_app_build_gradle()
    create_project_build_gradle()
    create_settings_gradle()
    create_gradle_wrapper_properties()
    create_gradle_wrapper()
    create_gradle_wrapper_bat()  # File batch untuk Windows
    create_proguard_rules()
    create_strings_xml()
    create_colors_xml()
    create_ic_launcher()
    create_ic_launcher_foreground()
    create_readme()
    
    print("\n✅ Semua file dan folder berhasil dibuat!")
    print("📁 Struktur project lengkap di direktori saat ini!")
    print("\n🔧 Untuk build APK, jalankan:")
    print("chmod +x gradlew")
    print("./gradlew assembleDebug")
    print("\n📱 APK akan tersedia di: app/build/outputs/apk/debug/")
def create_gradle_properties():
    content = '''org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.enableJetifier=true
android.nonTransitiveRClass=true
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.configureondemand=true
kotlin.code.style=official
'''
    
    file_path = 'gradle.properties'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")


def create_gradle_wrapper_properties():
    content = '''distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.1.1-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
'''
    
    file_path = 'gradle/wrapper/gradle-wrapper.properties'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")

def create_gradle_wrapper_bat():
    content = '''@rem
@rem Copyright 2015 the original author or authors.
@rem
@rem Licensed under the Apache License, Version 2.0 (the "License");
@rem you may not use this file except in compliance with the License.
@rem You may obtain a copy of the License at
@rem
@rem      https://www.apache.org/licenses/LICENSE-2.0
@rem
@rem Unless required by applicable law or agreed to in writing, software
@rem distributed under the License is distributed on an "AS IS" BASIS,
@rem WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@rem See the License for the specific language governing permissions and
@rem limitations under the License.
@rem

@if "%DEBUG%"=="" @echo off
@rem ##########################################################################
@rem
@rem  Gradle startup script for Windows
@rem
@rem ##########################################################################

@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%"=="" set DIRNAME=.
@rem This is normally unused
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%

@rem Resolve any "." and ".." in APP_HOME to make it shorter.
for %%i in ("%APP_HOME%") do set APP_HOME=%%~fi

@rem Add default JVM options here. You can also use JAVA_OPTS and GRADLE_OPTS to pass JVM options to this script.
set DEFAULT_JVM_OPTS="-Xmx64m" "-Xms64m"

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if %ERRORLEVEL% equ 0 goto execute

echo.
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto execute

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:execute
@rem Setup the command line

set CLASSPATH=%APP_HOME%\gradle\wrapper\gradle-wrapper.jar


@rem Execute Gradle
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %GRADLE_OPTS% -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*

:end
@rem End local scope for the variables with windows NT shell
if %ERRORLEVEL% equ 0 goto mainEnd

:fail
rem Set variable GRADLE_EXIT_CONSOLE if you need the _script_ return code instead of
rem the _cmd_ / _process_ return code!
set EXIT_CODE=%ERRORLEVEL%
if %EXIT_CODE% equ 0 set EXIT_CODE=1
if not ""=="%GRADLE_EXIT_CONSOLE%" exit %EXIT_CODE%
exit /b %EXIT_CODE%

:mainEnd
if "%OS%"=="Windows_NT" endlocal

:omega
'''
    
    file_path = 'gradlew.bat'
    with open(file_path, 'w', newline='\r\n') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")

def create_main_activity():
    content = '''package com.example.screenshotapp

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
        val permissions = mutableListOf<String>()

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) 
            != PackageManager.PERMISSION_GRANTED) {
            if (Build.VERSION.SDK_INT < Build.VERSION_CODES.Q) {
                permissions.add(Manifest.permission.WRITE_EXTERNAL_STORAGE)
            }
        }

        if (permissions.isNotEmpty()) {
            ActivityCompat.requestPermissions(this, permissions.toTypedArray(), PERMISSION_REQUEST_CODE)
        } else {
            checkOverlayPermission()
        }
    }

    private fun checkOverlayPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (!Settings.canDrawOverlays(this)) {
                val intent = Intent(
                    Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                    Uri.parse("package:$packageName")
                )
                startActivityForResult(intent, OVERLAY_PERMISSION_REQUEST_CODE)
            } else {
                startFloatingService()
            }
        } else {
            startFloatingService()
        }
    }

    private fun startFloatingService() {
        val intent = Intent(this, FloatingWindowService::class.java)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
        Toast.makeText(this, "Service dimulai", Toast.LENGTH_SHORT).show()
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
                checkOverlayPermission()
            } else {
                Toast.makeText(this, "Permission diperlukan", Toast.LENGTH_LONG).show()
                finish()
            }
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == OVERLAY_PERMISSION_REQUEST_CODE) {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                if (Settings.canDrawOverlays(this)) {
                    startFloatingService()
                } else {
                    Toast.makeText(this, "Overlay permission diperlukan", Toast.LENGTH_LONG).show()
                    finish()
                }
            }
        }
    }
}'''
    
    file_path = 'app/src/main/java/com/example/screenshotapp/MainActivity.kt'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")

def create_floating_window_service():
    content = '''package com.example.screenshotapp

import android.app.*
import android.content.Context
import android.content.Intent
import android.graphics.*
import android.hardware.display.DisplayManager
import android.hardware.display.VirtualDisplay
import android.media.Image
import android.media.ImageReader
import android.media.projection.MediaProjection
import android.media.projection.MediaProjectionManager
import android.os.Build
import android.os.Handler
import android.os.IBinder
import android.os.Looper
import android.util.DisplayMetrics
import android.view.*
import android.widget.*
import androidx.core.app.NotificationCompat
import java.io.File
import java.io.FileOutputStream
import java.nio.ByteBuffer

class FloatingWindowService : Service() {

    private lateinit var windowManager: WindowManager
    private lateinit var floatingView: View
    private lateinit var overlayView: View
    private lateinit var params: WindowManager.LayoutParams
    private lateinit var overlayParams: WindowManager.LayoutParams
    
    private var isOverlayVisible = false
    private val rectangles = mutableListOf<RectangleData>()
    private var currentRectIndex = 1
    private var imageName = "screenshot"
    
    private var mediaProjection: MediaProjection? = null
    private var imageReader: ImageReader? = null
    private var virtualDisplay: VirtualDisplay? = null
    
    companion object {
        const val MEDIA_PROJECTION_REQUEST_CODE = 200
        var mediaProjectionResultCode: Int = 0
        var mediaProjectionData: Intent? = null
    }

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        startForeground(1, createNotification())
        
        windowManager = getSystemService(Context.WINDOW_SERVICE) as WindowManager
        createFloatingButtons()
    }

    private fun createFloatingButtons() {
        floatingView = LayoutInflater.from(this).inflate(R.layout.floating_buttons, null)
        
        val layoutType = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        } else {
            WindowManager.LayoutParams.TYPE_PHONE
        }
        
        params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            layoutType,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = 100
            y = 100
        }
        
        windowManager.addView(floatingView, params)
        setupButtonListeners()
    }

    private fun setupButtonListeners() {
        val btnCrop = floatingView.findViewById<Button>(R.id.btnCrop)
        val btnSave = floatingView.findViewById<Button>(R.id.btnSave)
        val btnName = floatingView.findViewById<Button>(R.id.btnName)
        val btnClose = floatingView.findViewById<Button>(R.id.btnClose)
        
        btnCrop.setOnClickListener {
            if (!isOverlayVisible) {
                showOverlay()
            }
        }
        
        btnSave.setOnClickListener {
            if (rectangles.isNotEmpty()) {
                captureAndSaveScreenshots()
            } else {
                Toast.makeText(this, "Buat rectangle terlebih dahulu", Toast.LENGTH_SHORT).show()
            }
        }
        
        btnName.setOnClickListener {
            showNameDialog()
        }
        
        btnClose.setOnClickListener {
            stopSelf()
        }
        
        setupDraggable(floatingView, params)
    }

    private fun showOverlay() {
        overlayView = LayoutInflater.from(this).inflate(R.layout.overlay_layout, null)
        
        val layoutType = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        } else {
            WindowManager.LayoutParams.TYPE_PHONE
        }
        
        overlayParams = WindowManager.LayoutParams(
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.MATCH_PARENT,
            layoutType,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        )
        
        windowManager.addView(overlayView, overlayParams)
        isOverlayVisible = true
        
        setupOverlayListeners()
    }

    private fun setupOverlayListeners() {
        val canvas = overlayView.findViewById<OverlayCanvas>(R.id.overlayCanvas)
        val btnDone = overlayView.findViewById<Button>(R.id.btnDone)
        
        canvas.setRectangles(rectangles)
        canvas.setRectNumberStart(currentRectIndex)
        canvas.onRectangleCreated = { rectData ->
            rectangles.add(rectData)
            currentRectIndex++
        }
        canvas.onRectangleDeleted = { rectData ->
            rectangles.remove(rectData)
        }
        
        btnDone.setOnClickListener {
            hideOverlay()
        }
    }

    private fun hideOverlay() {
        if (isOverlayVisible) {
            windowManager.removeView(overlayView)
            isOverlayVisible = false
        }
    }

    private fun showNameDialog() {
        val dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_name, null)
        val editText = dialogView.findViewById<EditText>(R.id.etName)
        editText.setText(imageName)
        
        val dialog = AlertDialog.Builder(this, R.style.Theme_AppCompat_Dialog)
            .setTitle("Nama Gambar")
            .setView(dialogView)
            .setPositiveButton("OK") { _, _ ->
                imageName = editText.text.toString().ifEmpty { "screenshot" }
            }
            .setNegativeButton("Batal", null)
            .create()
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            dialog.window?.setType(WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY)
        } else {
            dialog.window?.setType(WindowManager.LayoutParams.TYPE_PHONE)
        }
        
        dialog.show()
    }

    private fun captureAndSaveScreenshots() {
        if (mediaProjectionData == null) {
            requestMediaProjection()
            return
        }
        
        startScreenCapture()
        
        Handler(Looper.getMainLooper()).postDelayed({
            val bitmap = captureScreen()
            if (bitmap != null) {
                saveCroppedImages(bitmap)
                stopScreenCapture()
            }
        }, 500)
    }

    private fun requestMediaProjection() {
        val intent = Intent(this, MediaProjectionActivity::class.java)
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        startActivity(intent)
    }

    private fun startScreenCapture() {
        val metrics = DisplayMetrics()
        windowManager.defaultDisplay.getMetrics(metrics)
        
        imageReader = ImageReader.newInstance(
            metrics.widthPixels,
            metrics.heightPixels,
            PixelFormat.RGBA_8888,
            2
        )
        
        val projectionManager = getSystemService(Context.MEDIA_PROJECTION_SERVICE) as MediaProjectionManager
        mediaProjection = projectionManager.getMediaProjection(mediaProjectionResultCode, mediaProjectionData!!)
        
        virtualDisplay = mediaProjection?.createVirtualDisplay(
            "ScreenCapture",
            metrics.widthPixels,
            metrics.heightPixels,
            metrics.densityDpi,
            DisplayManager.VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR,
            imageReader?.surface,
            null,
            null
        )
    }

    private fun captureScreen(): Bitmap? {
        val image = imageReader?.acquireLatestImage() ?: return null
        
        val planes = image.planes
        val buffer: ByteBuffer = planes[0].buffer
        val pixelStride = planes[0].pixelStride
        val rowStride = planes[0].rowStride
        val rowPadding = rowStride - pixelStride * image.width
        
        val bitmap = Bitmap.createBitmap(
            image.width + rowPadding / pixelStride,
            image.height,
            Bitmap.Config.ARGB_8888
        )
        bitmap.copyPixelsFromBuffer(buffer)
        image.close()
        
        return Bitmap.createBitmap(bitmap, 0, 0, image.width, image.height)
    }

    private fun saveCroppedImages(bitmap: Bitmap) {
        val dir = File(getExternalFilesDir(null), "Screenshots")
        if (!dir.exists()) dir.mkdirs()
        
        rectangles.forEach { rect ->
            try {
                val croppedBitmap = Bitmap.createBitmap(
                    bitmap,
                    rect.left.toInt(),
                    rect.top.toInt(),
                    (rect.right - rect.left).toInt(),
                    (rect.bottom - rect.top).toInt()
                )
                
                val fileName = "${imageName}_${String.format("%03d", rect.number)}.png"
                val file = File(dir, fileName)
                val fos = FileOutputStream(file)
                croppedBitmap.compress(Bitmap.CompressFormat.PNG, 100, fos)
                fos.close()
                
                Toast.makeText(this, "Saved: $fileName", Toast.LENGTH_SHORT).show()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
        
        bitmap.recycle()
    }

    private fun stopScreenCapture() {
        virtualDisplay?.release()
        mediaProjection?.stop()
        imageReader?.close()
    }

    private fun setupDraggable(view: View, params: WindowManager.LayoutParams) {
        var initialX = 0
        var initialY = 0
        var initialTouchX = 0f
        var initialTouchY = 0f
        
        view.setOnTouchListener { _, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
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
                    true
                }
                else -> false
            }
        }
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                "screenshot_service",
                "Screenshot Service",
                NotificationManager.IMPORTANCE_LOW
            )
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(channel)
        }
    }

    private fun createNotification(): Notification {
        return NotificationCompat.Builder(this, "screenshot_service")
            .setContentTitle("Screenshot App")
            .setContentText("Service berjalan")
            .setSmallIcon(android.R.drawable.ic_menu_camera)
            .build()
    }

    override fun onDestroy() {
        super.onDestroy()
        if (::floatingView.isInitialized) {
            windowManager.removeView(floatingView)
        }
        if (isOverlayVisible) {
            windowManager.removeView(overlayView)
        }
        stopScreenCapture()
    }

    override fun onBind(intent: Intent?): IBinder? = null
}

data class RectangleData(
    var left: Float,
    var top: Float,
    var right: Float,
    var bottom: Float,
    var number: Int
)'''
    
    file_path = 'app/src/main/java/com/example/screenshotapp/FloatingWindowService.kt'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")

def create_overlay_canvas():
    content = '''package com.example.screenshotapp

import android.app.AlertDialog
import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.os.Build
import android.util.AttributeSet
import android.view.LayoutInflater
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import android.widget.EditText

class OverlayCanvas @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0
) : View(context, attrs, defStyleAttr) {

    private val paint = Paint().apply {
        color = Color.RED
        strokeWidth = 5f
        style = Paint.Style.STROKE
    }
    
    private val textPaint = Paint().apply {
        color = Color.RED
        textSize = 40f
        style = Paint.Style.FILL
    }
    
    private val fillPaint = Paint().apply {
        color = Color.argb(50, 255, 0, 0)
        style = Paint.Style.FILL
    }

    private var rectangles = mutableListOf<RectangleData>()
    private var currentRect: RectangleData? = null
    private var startX = 0f
    private var startY = 0f
    private var isDrawing = false
    
    private var selectedRect: RectangleData? = null
    private var isDragging = false
    private var isResizing = false
    private var dragOffsetX = 0f
    private var dragOffsetY = 0f
    
    private var lastTapTime = 0L
    private var lastTapRect: RectangleData? = null
    
    private var rectNumberStart = 1
    
    var onRectangleCreated: ((RectangleData) -> Unit)? = null
    var onRectangleDeleted: ((RectangleData) -> Unit)? = null

    fun setRectangles(rects: MutableList<RectangleData>) {
        rectangles = rects
        invalidate()
    }
    
    fun setRectNumberStart(start: Int) {
        rectNumberStart = start
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        
        rectangles.forEach { rect ->
            canvas.drawRect(rect.left, rect.top, rect.right, rect.bottom, fillPaint)
            canvas.drawRect(rect.left, rect.top, rect.right, rect.bottom, paint)
            
            val number = String.format("%03d", rect.number)
            val textX = rect.left + 10
            val textY = rect.top + 50
            canvas.drawText(number, textX, textY, textPaint)
            
            drawResizeHandles(canvas, rect)
        }
        
        currentRect?.let { rect ->
            canvas.drawRect(rect.left, rect.top, rect.right, rect.bottom, fillPaint)
            canvas.drawRect(rect.left, rect.top, rect.right, rect.bottom, paint)
        }
    }
    
    private fun drawResizeHandles(canvas: Canvas, rect: RectangleData) {
        val handleSize = 30f
        val handlePaint = Paint().apply {
            color = Color.BLUE
            style = Paint.Style.FILL
        }
        
        canvas.drawCircle(rect.left, rect.top, handleSize, handlePaint)
        canvas.drawCircle(rect.right, rect.top, handleSize, handlePaint)
        canvas.drawCircle(rect.left, rect.bottom, handleSize, handlePaint)
        canvas.drawCircle(rect.right, rect.bottom, handleSize, handlePaint)
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        when (event.action) {
            MotionEvent.ACTION_DOWN -> {
                val x = event.x
                val y = event.y
                
                val tappedRect = findRectangleAt(x, y)
                if (tappedRect != null) {
                    val currentTime = System.currentTimeMillis()
                    if (currentTime - lastTapTime < 300 && tappedRect == lastTapRect) {
                        showRectangleOptions(tappedRect)
                        lastTapTime = 0
                        lastTapRect = null
                        return true
                    }
                    lastTapTime = currentTime
                    lastTapRect = tappedRect
                    
                    val resizeCorner = findResizeCorner(x, y, tappedRect)
                    if (resizeCorner != null) {
                        selectedRect = tappedRect
                        isResizing = true
                        startX = x
                        startY = y
                    } else {
                        selectedRect = tappedRect
                        isDragging = true
                        dragOffsetX = x - tappedRect.left
                        dragOffsetY = y - tappedRect.top
                    }
                } else {
                    startX = x
                    startY = y
                    currentRect = RectangleData(x, y, x, y, rectNumberStart)
                    isDrawing = true
                }
            }
            
            MotionEvent.ACTION_MOVE -> {
                val x = event.x
                val y = event.y
                
                when {
                    isDrawing -> {
                        currentRect?.right = x
                        currentRect?.bottom = y
                        invalidate()
                    }
                    isDragging -> {
                        selectedRect?.let { rect ->
                            val width = rect.right - rect.left
                            val height = rect.bottom - rect.top
                            rect.left = x - dragOffsetX
                            rect.top = y - dragOffsetY
                            rect.right = rect.left + width
                            rect.bottom = rect.top + height
                            invalidate()
                        }
                    }
                    isResizing -> {
                        selectedRect?.let { rect ->
                            val dx = x - startX
                            val dy = y - startY
                            
                            when (findResizeCorner(startX, startY, rect)) {
                                "topLeft" -> {
                                    rect.left += dx
                                    rect.top += dy
                                }
                                "topRight" -> {
                                    rect.right += dx
                                    rect.top += dy
                                }
                                "bottomLeft" -> {
                                    rect.left += dx
                                    rect.bottom += dy
                                }
                                "bottomRight" -> {
                                    rect.right += dx
                                    rect.bottom += dy
                                }
                            }
                            
                            startX = x
                            startY = y
                            invalidate()
                        }
                    }
                }
            }
            
            MotionEvent.ACTION_UP -> {
                if (isDrawing) {
                    currentRect?.let { rect ->
                        normalizeRect(rect)
                        rectangles.add(rect)
                        onRectangleCreated?.invoke(rect)
                        rectNumberStart++
                    }
                    currentRect = null
                    isDrawing = false
                }
                
                isDragging = false
                isResizing = false
                selectedRect = null
                invalidate()
            }
        }
        return true
    }
    
    private fun normalizeRect(rect: RectangleData) {
        if (rect.left > rect.right) {
            val temp = rect.left
            rect.left = rect.right
            rect.right = temp
        }
        if (rect.top > rect.bottom) {
            val temp = rect.top
            rect.top = rect.bottom
            rect.bottom = temp
        }
    }
    
    private fun findRectangleAt(x: Float, y: Float): RectangleData? {
        return rectangles.lastOrNull { rect ->
            x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom
        }
    }
    
    private fun findResizeCorner(x: Float, y: Float, rect: RectangleData): String? {
        val handleSize = 30f
        
        return when {
            isNear(x, rect.left, handleSize) && isNear(y, rect.top, handleSize) -> "topLeft"
            isNear(x, rect.right, handleSize) && isNear(y, rect.top, handleSize) -> "topRight"
            isNear(x, rect.left, handleSize) && isNear(y, rect.bottom, handleSize) -> "bottomLeft"
            isNear(x, rect.right, handleSize) && isNear(y, rect.bottom, handleSize) -> "bottomRight"
            else -> null
        }
    }
    
    private fun isNear(value: Float, target: Float, threshold: Float): Boolean {
        return Math.abs(value - target) <= threshold
    }
    
    private fun showRectangleOptions(rect: RectangleData) {
        val options = arrayOf("Renumber", "Delete")
        
        val builder = AlertDialog.Builder(context, androidx.appcompat.R.style.Theme_AppCompat_Dialog)
        builder.setTitle("Rectangle ${String.format("%03d", rect.number)}")
        builder.setItems(options) { _, which ->
            when (which) {
                0 -> showRenumberDialog(rect)
                1 -> deleteRectangle(rect)
            }
        }
        
        val dialog = builder.create()
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            dialog.window?.setType(WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY)
        } else {
            dialog.window?.setType(WindowManager.LayoutParams.TYPE_PHONE)
        }
        
        dialog.show()
    }
    
    private fun showRenumberDialog(rect: RectangleData) {
        val dialogView = LayoutInflater.from(context).inflate(R.layout.dialog_name, null)
        val editText = dialogView.findViewById<EditText>(R.id.etName)
        editText.setText(rect.number.toString())
        editText.hint = "Nomor baru"
        
        val dialog = AlertDialog.Builder(context, androidx.appcompat.R.style.Theme_AppCompat_Dialog)
            .setTitle("Renumber Rectangle")
            .setView(dialogView)
            .setPositiveButton("OK") { _, _ ->
                val newNumber = editText.text.toString().toIntOrNull()
                if (newNumber != null && newNumber > 0) {
                    rect.number = newNumber
                    invalidate()
                }
            }
            .setNegativeButton("Batal", null)
            .create()
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            dialog.window?.setType(WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY)
        } else {
            dialog.window?.setType(WindowManager.LayoutParams.TYPE_PHONE)
        }
        
        dialog.show()
    }
    
    private fun deleteRectangle(rect: RectangleData) {
        rectangles.remove(rect)
        onRectangleDeleted?.invoke(rect)
        invalidate()
    }
}'''
    
    file_path = 'app/src/main/java/com/example/screenshotapp/OverlayCanvas.kt'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")

def create_media_projection_activity():
    content = '''package com.example.screenshotapp

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.media.projection.MediaProjectionManager
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class MediaProjectionActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val projectionManager = getSystemService(Context.MEDIA_PROJECTION_SERVICE) as MediaProjectionManager
        startActivityForResult(
            projectionManager.createScreenCaptureIntent(),
            FloatingWindowService.MEDIA_PROJECTION_REQUEST_CODE
        )
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        
        if (requestCode == FloatingWindowService.MEDIA_PROJECTION_REQUEST_CODE) {
            if (resultCode == Activity.RESULT_OK && data != null) {
                FloatingWindowService.mediaProjectionResultCode = resultCode
                FloatingWindowService.mediaProjectionData = data
            }
            finish()
        }
    }
}'''
    
    file_path = 'app/src/main/java/com/example/screenshotapp/MediaProjectionActivity.kt'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")

def create_activity_main_xml():
    content = '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center"
    android:orientation="vertical"
    android:padding="16dp">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Screenshot App"
        android:textSize="24sp"
        android:textStyle="bold"
        android:layout_marginBottom="16dp"/>

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Aplikasi akan dimulai..."
        android:textSize="16sp"/>

</LinearLayout>'''
    
    file_path = 'app/src/main/res/layout/activity_main.xml'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")

def create_floating_buttons_xml():
    content = '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:background="#80000000"
    android:padding="8dp">

    <Button
        android:id="@+id/btnCrop"
        android:layout_width="120dp"
        android:layout_height="48dp"
        android:text="CROP"
        android:textSize="14sp"
        android:layout_marginBottom="4dp"/>

    <Button
        android:id="@+id/btnSave"
        android:layout_width="120dp"
        android:layout_height="48dp"
        android:text="SAVE"
        android:textSize="14sp"
        android:layout_marginBottom="4dp"/>

    <Button
        android:id="@+id/btnName"
        android:layout_width="120dp"
        android:layout_height="48dp"
        android:text="NAMA"
        android:textSize="14sp"
        android:layout_marginBottom="4dp"/>

    <Button
        android:id="@+id/btnClose"
        android:layout_width="120dp"
        android:layout_height="48dp"
        android:text="CLOSE"
        android:textSize="14sp"
        android:backgroundTint="#CC0000"/>

</LinearLayout>'''
    
    file_path = 'app/src/main/res/layout/floating_buttons.xml'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")

def create_overlay_layout_xml():
    content = '''<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#00000000">

    <com.example.screenshotapp.OverlayCanvas
        android:id="@+id/overlayCanvas"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />

    <Button
        android:id="@+id/btnDone"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="DONE"
        android:layout_alignParentBottom="true"
        android:layout_centerHorizontal="true"
        android:layout_marginBottom="16dp"
        android:padding="16dp"
        android:textSize="16sp"
        android:backgroundTint="#4CAF50"/>

</RelativeLayout>'''
    
    file_path = 'app/src/main/res/layout/overlay_layout.xml'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")

def create_dialog_name_xml():
    content = '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:padding="16dp">

    <EditText
        android:id="@+id/etName"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Masukkan nama gambar"
        android:inputType="text"
        android:maxLines="1"
        android:padding="12dp"/>

</LinearLayout>'''
    
    file_path = 'app/src/main/res/layout/dialog_name.xml'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")

def create_android_manifest():
    content = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.screenshotapp">

    <uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/Theme.AppCompat.Light.DarkActionBar">
        
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <activity
            android:name=".MediaProjectionActivity"
            android:theme="@style/Theme.AppCompat.Translucent" />

        <service
            android:name=".FloatingWindowService"
            android:enabled="true"
            android:exported="true" />
    </application>

</manifest>'''
    
    file_path = 'app/src/main/AndroidManifest.xml'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")


def create_app_build_gradle():
    content = '''plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.example.screenshotapp'
    compileSdk 34

    defaultConfig {
        applicationId "com.example.screenshotapp"
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "1.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
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
    implementation 'com.google.android.material:material:1.10.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'androidx.lifecycle:lifecycle-service:2.7.0'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}'''
    
    file_path = 'app/build.gradle'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")


def create_project_build_gradle():
    content = '''// Top-level build file where you can add configuration options common to all sub-projects/modules.
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.1.4'
        classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:1.9.0'
    }
}

// NOTE:
// Bagian allprojects {} DIHAPUS agar tidak conflict dengan
// repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
// di settings.gradle

task clean(type: Delete) {
    delete rootProject.buildDir
}
'''
    
    file_path = 'build.gradle'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")



def create_settings_gradle():
    content = '''pluginManagement {
    repositories {
        gradlePluginPortal()
        google()
        mavenCentral()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "ScreenshotApp"
include ':app'
'''
    
    file_path = 'settings.gradle'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")
    

def create_gradle_wrapper():
    gradlew_content = '''#!/bin/sh

# Gradle wrapper script untuk Android projects

# Set JAVA_HOME jika belum diset
if [ -z "$JAVA_HOME" ]; then
    if command -v java >/dev/null 2>&1; then
        JAVA_HOME=$(dirname $(dirname $(readlink -f $(command -v java))))
    fi
fi

# Eksekusi Gradle wrapper
exec java -Xmx64m -Xms64m -cp "$APP_HOME/gradle/wrapper/gradle-wrapper.jar" org.gradle.wrapper.GradleWrapperMain "$@"
'''
    
    file_path = 'gradlew'
    with open(file_path, 'w', newline='\n') as f:
        f.write(gradlew_content)
    os.chmod(file_path, 0o755)
    print(f"📄 Created file: {file_path}")

def create_strings_xml():
    content = '''<resources>
    <string name="app_name">Screenshot App</string>
</resources>'''
    
    file_path = 'app/src/main/res/values/strings.xml'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")

def create_colors_xml():
    content = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
</resources>'''
    
    file_path = 'app/src/main/res/values/colors.xml'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")

def create_ic_launcher():
    content = '''<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp"
    android:height="24dp"
    android:viewportWidth="24"
    android:viewportHeight="24">
  <path
      android:fillColor="#FF000000"
      android:pathData="M12,2A10,10 0,0 0,2 12A10,10 0,0 0,12 22A10,10 0,0 0,22 12A10,10 0,0 0,12 2Z"/>
</vector>'''
    
    file_path = 'app/src/main/res/drawable/ic_launcher_background.xml'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")

def create_ic_launcher_foreground():
    content = '''<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp"
    android:height="24dp"
    android:viewportWidth="24"
    android:viewportHeight="24">
  <path
      android:fillColor="#FFFFFF"
      android:pathData="M12,2A10,10 0,0 0,2 12A10,10 0,0 0,12 22A10,10 0,0 0,22 12A10,10 0,0 0,12 2Z"/>
</vector>'''
    
    file_path = 'app/src/main/res/drawable/ic_launcher_foreground.xml'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")

def create_proguard_rules():
    content = '''# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.
#
# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

# If your project uses WebView with JS, uncomment the following
# and specify the fully qualified class name to the JavaScript interface
# class:
#-keepclassmembers class fqcn.of.javascript.interface.for.webview {
#   public *;
#}

# Uncomment this to preserve the line number information for
# debugging stack traces.
#-keepattributes SourceFile,LineNumberTable

# If you keep the line number information, uncomment this to
# hide the original source file name.
#-renamesourcefileattribute SourceFile
'''
    
    file_path = 'app/proguard-rules.pro'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")

def create_readme():
    content = '''# Screenshot App dengan Floating Windows

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
'''
    
    file_path = 'README.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created file: {file_path}")

if __name__ == "__main__":
    create_screenshot_app()