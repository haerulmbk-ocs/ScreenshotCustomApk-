package com.sshotcustom.app

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
