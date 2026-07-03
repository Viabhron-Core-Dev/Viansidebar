package com.example.service

import android.app.AlertDialog
import android.content.Context
import android.graphics.*
import android.graphics.drawable.Drawable
import android.os.Build
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.view.WindowManager
import android.widget.BaseAdapter
import android.widget.GridView
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView

fun showFolderStyleDialog(context: Context, item: SidebarItem.Folder, manager: SidebarAppsManager, onStyleSelected: ((Int) -> Unit)? = null) {
    val layout = LinearLayout(context).apply {
        orientation = LinearLayout.VERTICAL
        setPadding(40, 40, 40, 40)
        setBackgroundColor(Color.WHITE)
    }

    val title = TextView(context).apply {
        text = "Folder style"
        textSize = 20f
        typeface = Typeface.DEFAULT_BOLD
        setTextColor(Color.BLACK)
        setPadding(0, 0, 0, 40)
    }
    layout.addView(title)

    val gridView = GridView(context).apply {
        numColumns = 2
        verticalSpacing = 40
        horizontalSpacing = 20
    }

    val styles = listOf(
        "Grid", "Stack"
    )

    val adapter = object : BaseAdapter() {
        override fun getCount(): Int = styles.size
        override fun getItem(position: Int): Any = styles[position]
        override fun getItemId(position: Int): Long = position.toLong()
        override fun getView(position: Int, convertView: View?, parent: ViewGroup?): View {
            val view = convertView as? LinearLayout ?: LinearLayout(context).apply {
                orientation = LinearLayout.VERTICAL
                gravity = Gravity.CENTER
            }
            view.removeAllViews()

            val density = context.resources.displayMetrics.density
            val size = (64 * density).toInt()

            val iv = ImageView(context).apply {
                layoutParams = LinearLayout.LayoutParams(size, size)
                val miniIcons = item.items.mapNotNull { 
                    if (it.startsWith("app:")) manager.iconCache.get(it.substringAfter("app:")) else null 
                }
                setImageDrawable(FolderStyleDrawable(position, Color.parseColor("#00BFA5"), Color.parseColor("#333333"), miniIcons))
            }
            view.addView(iv)

            val tv = TextView(context).apply {
                text = styles[position]
                textSize = 12f
                gravity = Gravity.CENTER
                setTextColor(Color.BLACK)
                setPadding(0, 10, 0, 0)
                if (position == item.folderStyle) {
                    setTypeface(null, Typeface.BOLD)
                }
            }
            view.addView(tv)

            return view
        }
    }

    gridView.adapter = adapter
    layout.addView(gridView, LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT))

    val dialog = AlertDialog.Builder(context, android.R.style.Theme_DeviceDefault_Light_Dialog_Alert)
        .setView(layout)
        .setPositiveButton("OK", null)
        .create()

    gridView.setOnItemClickListener { _, _, position, _ ->
        if (onStyleSelected != null) {
            onStyleSelected(position)
        } else {
            val json = org.json.JSONObject().apply {
                put("name", item.name)
                put("colorHex", item.colorHex)
                val jArr = org.json.JSONArray()
                item.items.forEach { jArr.put(it) }
                put("items", jArr)
                put("folderStyle", position)
            }
            manager.removeItem(item.id)
            manager.addItem("folder:${item.uuid}:$json")
        }
        dialog.dismiss()
    }

    dialog.window?.setType(if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY else WindowManager.LayoutParams.TYPE_PHONE)
    dialog.show()
}

class FolderStyleDrawable(
    private val styleIndex: Int,
    private val themeColor: Int,
    private val iconColor: Int,
    private val miniIcons: List<Bitmap> = emptyList()
) : Drawable() {

    private val paint = Paint(Paint.ANTI_ALIAS_FLAG)
    private val iconPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { isFilterBitmap = true }
    
    override fun draw(canvas: Canvas) {
        val w = bounds.width().toFloat()
        val h = bounds.height().toFloat()
        val cx = bounds.centerX().toFloat()
        val cy = bounds.centerY().toFloat()
        
        paint.style = Paint.Style.FILL
        paint.color = themeColor
        paint.alpha = 100
        canvas.drawCircle(cx, cy, w / 2f, paint)

        val symbolSize = w * 0.6f
        val sx = cx - symbolSize / 2f
        val sy = cy - symbolSize / 2f
        
        paint.alpha = 255
        
        if (styleIndex == 1) {
            drawStack(canvas, sx, sy, symbolSize)
        } else {
            drawGrid(canvas, sx, sy, symbolSize)
        }
    }
    
    private fun drawGrid(canvas: Canvas, x: Float, y: Float, size: Float) {
        if (miniIcons.isEmpty()) {
            paint.style = Paint.Style.STROKE
            paint.strokeWidth = 4f
            canvas.drawRect(x + size*0.1f, y + size*0.2f, x + size*0.9f, y + size*0.8f, paint)
            canvas.drawLine(x + size*0.1f, y + size*0.4f, x + size*0.9f, y + size*0.4f, paint)
            return
        }
        val count = miniIcons.size
        
        if (count == 1) {
            val p = size * 0.1f
            val ix = x + p
            val iy = y + p
            val isize = size - 2*p
            canvas.drawBitmap(miniIcons[0], null, RectF(ix, iy, ix + isize, iy + isize), iconPaint)
        } else if (count == 2) {
            val padding = size * 0.05f
            val iconSize = (size - padding * 3) / 2f
            val startY = y + (size - iconSize) / 2f
            for (i in 0 until 2) {
                val ix = x + padding + i * (iconSize + padding)
                canvas.drawBitmap(miniIcons[i], null, RectF(ix, startY, ix + iconSize, startY + iconSize), iconPaint)
            }
        } else if (count <= 4) {
            val padding = size * 0.05f
            val iconSize = (size - padding * 3) / 2f
            for (i in 0 until count) {
                val row = i / 2
                val col = i % 2
                val ix = x + padding + col * (iconSize + padding)
                val iy = y + padding + row * (iconSize + padding)
                canvas.drawBitmap(miniIcons[i], null, RectF(ix, iy, ix + iconSize, iy + iconSize), iconPaint)
            }
        } else {
            // up to 9 (3x3 grid)
            val maxCount = minOf(9, count)
            val padding = size * 0.05f
            val iconSize = (size - padding * 4) / 3f
            for (i in 0 until maxCount) {
                val row = i / 3
                val col = i % 3
                val ix = x + padding + col * (iconSize + padding)
                val iy = y + padding + row * (iconSize + padding)
                canvas.drawBitmap(miniIcons[i], null, RectF(ix, iy, ix + iconSize, iy + iconSize), iconPaint)
            }
        }
    }
    
    private fun drawStack(canvas: Canvas, x: Float, y: Float, size: Float) {
        if (miniIcons.isEmpty()) {
            paint.style = Paint.Style.STROKE
            paint.strokeWidth = 4f
            canvas.drawRect(x + size*0.1f, y + size*0.2f, x + size*0.9f, y + size*0.8f, paint)
            canvas.drawLine(x + size*0.1f, y + size*0.4f, x + size*0.9f, y + size*0.4f, paint)
            return
        }
        val count = minOf(3, miniIcons.size)
        val gap = size * 0.15f
        val cardSize = size - gap * (count - 1)
        
        for (i in count - 1 downTo 0) {
            val tx = x + i * gap
            val ty = y + i * gap
            canvas.drawBitmap(miniIcons[i], null, RectF(tx, ty, tx + cardSize, ty + cardSize), iconPaint)
        }
    }

    override fun setAlpha(alpha: Int) {}
    override fun setColorFilter(colorFilter: ColorFilter?) {}
    @Suppress("OVERRIDE_DEPRECATION")
    override fun getOpacity(): Int = PixelFormat.TRANSLUCENT
}
