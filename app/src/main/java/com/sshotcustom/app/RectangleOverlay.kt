package com.sshotcustom.app

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
