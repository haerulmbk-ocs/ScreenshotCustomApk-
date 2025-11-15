package com.example.screenshotapp

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
)