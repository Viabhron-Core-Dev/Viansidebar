package com.example.service

import android.annotation.SuppressLint
import android.appwidget.AppWidgetManager
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.graphics.PixelFormat
import android.os.Build
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.view.WindowManager
import android.widget.Button
import android.widget.FrameLayout
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import androidx.recyclerview.widget.ItemTouchHelper
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.GridLayoutManager
import android.graphics.drawable.BitmapDrawable
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.drawable.Drawable

import androidx.recyclerview.widget.RecyclerView
import com.example.utils.AppWidgetHelper
import org.json.JSONArray
import java.util.Collections

@SuppressLint("ViewConstructor")
class WidgetsGridEditOverlayView(
    context: Context,
    private val pageId: String,
    private val windowManager: WindowManager,
    private val onAddClicked: () -> Unit,
    private val onClose: () -> Unit
) : FrameLayout(context) {

    private val layoutParams: WindowManager.LayoutParams
    private val recyclerView: RecyclerView
    private val adapter: WidgetEditAdapter
    private val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
    
    val localIds = mutableListOf<Int>()
    private val appWidgetManager = AppWidgetManager.getInstance(context)

    init {
        setBackgroundColor(Color.parseColor("#E6000000")) // Semi-transparent black

        layoutParams = WindowManager.LayoutParams(
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.MATCH_PARENT,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY else WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        )

        loadLocalIds()

        val mainLayout = LinearLayout(context).apply {
            orientation = LinearLayout.VERTICAL
            layoutParams = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
            setPadding(48, 48, 48, 48)
            gravity = Gravity.CENTER_HORIZONTAL
        }

        // Header
        val headerLayout = LinearLayout(context).apply {
            orientation = LinearLayout.HORIZONTAL
            layoutParams = LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT)
            gravity = Gravity.CENTER_VERTICAL
            setPadding(0, 0, 0, 32)
        }

        val titleView = TextView(context).apply {
            text = "Edit Widgets Grid"
            setTextColor(Color.WHITE)
            textSize = 24f
            layoutParams = LinearLayout.LayoutParams(0, LayoutParams.WRAP_CONTENT, 1f)
        }

        val btnClose = Button(context).apply {
            text = "Done"
            setOnClickListener {
                saveIds()
                onClose()
            }
        }

        headerLayout.addView(titleView)
        headerLayout.addView(btnClose)
        mainLayout.addView(headerLayout)

        // Recycler View for drag-and-drop
        adapter = WidgetEditAdapter()
        recyclerView = RecyclerView(context).apply {
            layoutParams = LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, 0, 1f)
            val columns = prefs.getInt("sidebar_columns", 3)
            layoutManager = GridLayoutManager(context, columns)
            this.adapter = this@WidgetsGridEditOverlayView.adapter
        }
        mainLayout.addView(recyclerView)

        // Add Widget Button
        val btnAdd = Button(context).apply {
            text = "Add Widget"
            layoutParams = LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT).apply {
                topMargin = 32
            }
            setOnClickListener {
                saveIds() // Save before leaving
                onAddClicked()
            }
        }
        mainLayout.addView(btnAdd)

        addView(mainLayout)

        setupItemTouchHelper()
    }

    private fun loadLocalIds() {
        val jsonStr = prefs.getString("widgets_grid_$pageId", "[]") ?: "[]"
        val arr = JSONArray(jsonStr)
        localIds.clear()
        for (i in 0 until arr.length()) {
            localIds.add(arr.getInt(i))
        }
    }

    private fun saveIds() {
        val arr = JSONArray()
        localIds.forEach { arr.put(it) }
        prefs.edit().putString("widgets_grid_$pageId", arr.toString()).apply()
        
        // Notify grid to update
        val intent = Intent("WIDGET_ADDED_TO_GRID") // We can use the same intent to trigger reload
        intent.putExtra("PAGE_ID", pageId)
        context.sendBroadcast(intent)
    }

    private val receiver = object : android.content.BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            if (intent?.action == "WIDGET_ADDED_TO_GRID") {
                refresh()
            }
        }
    }

    fun attach() {
        try {
            windowManager.addView(this, layoutParams)
            context.registerReceiver(receiver, android.content.IntentFilter("WIDGET_ADDED_TO_GRID"), Context.RECEIVER_NOT_EXPORTED)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun detach() {
        try {
            windowManager.removeView(this)
            try { context.unregisterReceiver(receiver) } catch (e: Exception) {}
        } catch (e: Exception) {}
    }

    fun refresh() {
        loadLocalIds()
        adapter.notifyDataSetChanged()
    }

    private fun setupItemTouchHelper() {
        val callback = object : ItemTouchHelper.SimpleCallback(ItemTouchHelper.UP or ItemTouchHelper.DOWN or ItemTouchHelper.LEFT or ItemTouchHelper.RIGHT, 0) {
            override fun onMove(
                recyclerView: RecyclerView,
                viewHolder: RecyclerView.ViewHolder,
                target: RecyclerView.ViewHolder
            ): Boolean {
                val fromPos = viewHolder.adapterPosition
                val toPos = target.adapterPosition
                Collections.swap(localIds, fromPos, toPos)
                adapter.notifyItemMoved(fromPos, toPos)
                return true
            }

            override fun onSwiped(viewHolder: RecyclerView.ViewHolder, direction: Int) {}
            override fun isLongPressDragEnabled(): Boolean = true
            override fun clearView(recyclerView: RecyclerView, viewHolder: RecyclerView.ViewHolder) {
                super.clearView(recyclerView, viewHolder)
                saveIds()
            }
        }
        ItemTouchHelper(callback).attachToRecyclerView(recyclerView)
    }

    inner class WidgetEditAdapter : RecyclerView.Adapter<WidgetEditAdapter.ViewHolder>() {

        inner class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
            val tvName: TextView = view.findViewById(1)
            val btnRemove: ImageView = view.findViewById(2)
            val dragHandle: ImageView = view.findViewById(3)
        }

        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
            val layout = LinearLayout(context).apply {
                orientation = LinearLayout.HORIZONTAL
                layoutParams = RecyclerView.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT).apply { setMargins(0, 0, 0, 8) }
                gravity = Gravity.CENTER_VERTICAL
                setPadding(16, 24, 16, 24)
                setBackgroundColor(Color.parseColor("#33FFFFFF"))
            }

            val dragHandle = ImageView(context).apply {
                id = 3
                setImageResource(android.R.drawable.ic_menu_sort_by_size)
                setColorFilter(Color.WHITE)
                setPadding(16, 16, 16, 16)
            }

            val tvName = TextView(context).apply {
                id = 1
                setTextColor(Color.WHITE)
                textSize = 18f
                layoutParams = LinearLayout.LayoutParams(0, LayoutParams.WRAP_CONTENT, 1f).apply {
                    marginStart = 16
                }
            }

            val btnRemove = ImageView(context).apply {
                id = 2
                setImageResource(android.R.drawable.ic_menu_delete)
                setColorFilter(Color.RED)
                setPadding(16, 16, 16, 16)
            }

            layout.addView(dragHandle)
            layout.addView(tvName)
            layout.addView(btnRemove)

            return ViewHolder(layout)
        }

        override fun onBindViewHolder(holder: ViewHolder, position: Int) {
            val widgetId = localIds[position]
            val info = appWidgetManager.getAppWidgetInfo(widgetId)
            
            holder.tvName.text = info?.loadLabel(context.packageManager) ?: "Widget $widgetId (Unknown)"

            holder.btnRemove.setOnClickListener {
                val pos = holder.adapterPosition
                if (pos != RecyclerView.NO_POSITION) {
                    val removedId = localIds.removeAt(pos)
                    notifyItemRemoved(pos)
                    saveIds()
                    
                    // Also delete from host
                    try {
                        AppWidgetHelper.getHost(context).deleteAppWidgetId(removedId)
                    } catch (e: Exception) {}
                }
            }
        }

        override fun getItemCount(): Int = localIds.size
    }
}
