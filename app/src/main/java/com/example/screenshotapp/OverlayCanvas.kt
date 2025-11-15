package com.example.screenshotapp

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
}