import sys

new_content = """package com.example.service

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
import androidx.recyclerview.widget.RecyclerView
import com.example.utils.AppWidgetHelper
import org.json.JSONArray
import org.json.JSONObject
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
    
    val localItems = mutableListOf<GridWidgetItem>()
    private val appWidgetManager = AppWidgetManager.getInstance(context)
    
    // Preview container
    private val previewContainer = FrameLayout(context)

    init {
        setBackgroundColor(Color.parseColor("#F2000000")) // Darker semi-transparent black
        
        layoutParams = WindowManager.LayoutParams(
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.MATCH_PARENT,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY else WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        )

        loadLocalItems()

        val mainLayout = LinearLayout(context).apply {
            orientation = LinearLayout.VERTICAL
            layoutParams = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
            setPadding(32, 32, 32, 32)
            gravity = Gravity.CENTER_HORIZONTAL
        }

        // Header
        val headerLayout = LinearLayout(context).apply {
            orientation = LinearLayout.HORIZONTAL
            layoutParams = LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT)
            gravity = Gravity.CENTER_VERTICAL
            setPadding(0, 0, 0, 16)
        }

        val titleView = TextView(context).apply {
            text = "Edit Widgets Grid"
            setTextColor(Color.WHITE)
            textSize = 20f
            layoutParams = LinearLayout.LayoutParams(0, LayoutParams.WRAP_CONTENT, 1f)
        }

        val btnClose = Button(context).apply {
            text = "Done"
            setOnClickListener {
                saveItems()
                onClose()
            }
        }

        headerLayout.addView(titleView)
        headerLayout.addView(btnClose)
        mainLayout.addView(headerLayout)
        
        // Grid Total Size Editor
        val gridTotalLayout = LinearLayout(context).apply {
            orientation = LinearLayout.HORIZONTAL
            layoutParams = LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT)
            gravity = Gravity.CENTER_VERTICAL
            setPadding(0, 0, 0, 16)
        }
        
        var totalCols = prefs.getInt("widgets_grid_cols_$pageId", 4)
        
        val tvTotalCols = TextView(context).apply {
            text = "Grid Columns: $totalCols"
            setTextColor(Color.WHITE)
            layoutParams = LinearLayout.LayoutParams(0, LayoutParams.WRAP_CONTENT, 1f)
        }
        
        val btnMinusCol = Button(context).apply {
            text = "-"
            setOnClickListener {
                if (totalCols > 1) {
                    totalCols--
                    prefs.edit().putInt("widgets_grid_cols_$pageId", totalCols).apply()
                    tvTotalCols.text = "Grid Columns: $totalCols"
                    updatePreview()
                }
            }
        }
        
        val btnPlusCol = Button(context).apply {
            text = "+"
            setOnClickListener {
                if (totalCols < 10) {
                    totalCols++
                    prefs.edit().putInt("widgets_grid_cols_$pageId", totalCols).apply()
                    tvTotalCols.text = "Grid Columns: $totalCols"
                    updatePreview()
                }
            }
        }
        
        gridTotalLayout.addView(tvTotalCols)
        gridTotalLayout.addView(btnMinusCol)
        gridTotalLayout.addView(btnPlusCol)
        mainLayout.addView(gridTotalLayout)
        
        // Preview Box
        previewContainer.layoutParams = LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, 0, 0.4f).apply {
            setMargins(0, 16, 0, 16)
        }
        previewContainer.setBackgroundColor(Color.parseColor("#22FFFFFF")) // slight white bg for the block
        mainLayout.addView(previewContainer)
        updatePreview()

        // Recycler View for drag-and-drop & editing sizes
        adapter = WidgetEditAdapter()
        recyclerView = RecyclerView(context).apply {
            layoutParams = LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, 0, 0.6f)
            layoutManager = LinearLayoutManager(context)
            this.adapter = this@WidgetsGridEditOverlayView.adapter
        }
        mainLayout.addView(recyclerView)

        // Add Widget Button
        val btnAdd = Button(context).apply {
            text = "Add Widget"
            layoutParams = LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT).apply {
                topMargin = 16
            }
            setOnClickListener {
                saveItems() 
                onAddClicked()
            }
        }
        mainLayout.addView(btnAdd)

        addView(mainLayout)
        setupItemTouchHelper()
    }
    
    private fun updatePreview() {
        previewContainer.removeAllViews()
        val pagePreview = WidgetsGridPageView(context, pageId) {}
        previewContainer.addView(pagePreview)
    }

    private fun loadLocalItems() {
        val jsonStr = prefs.getString("widgets_grid_$pageId", "[]") ?: "[]"
        val arr = JSONArray(jsonStr)
        localItems.clear()
        for (i in 0 until arr.length()) {
            val obj = arr.optJSONObject(i)
            if (obj != null) {
                localItems.add(GridWidgetItem(
                    obj.getInt("id"),
                    obj.optInt("cols", 2),
                    obj.optInt("rows", 2)
                ))
            } else {
                val id = arr.optInt(i, -1)
                if (id != -1) {
                    localItems.add(GridWidgetItem(id, 2, 2))
                }
            }
        }
    }

    private fun saveItems() {
        val arr = JSONArray()
        localItems.forEach { 
            val obj = JSONObject()
            obj.put("id", it.id)
            obj.put("cols", it.cols)
            obj.put("rows", it.rows)
            arr.put(obj)
        }
        prefs.edit().putString("widgets_grid_$pageId", arr.toString()).apply()
        
        // Notify grid to update
        val intent = Intent("WIDGET_ADDED_TO_GRID")
        intent.putExtra("PAGE_ID", pageId)
        context.sendBroadcast(intent)
        
        updatePreview()
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
        loadLocalItems()
        adapter.notifyDataSetChanged()
        updatePreview()
    }

    private fun setupItemTouchHelper() {
        val callback = object : ItemTouchHelper.SimpleCallback(ItemTouchHelper.UP or ItemTouchHelper.DOWN, 0) {
            override fun onMove(
                recyclerView: RecyclerView,
                viewHolder: RecyclerView.ViewHolder,
                target: RecyclerView.ViewHolder
            ): Boolean {
                val fromPos = viewHolder.adapterPosition
                val toPos = target.adapterPosition
                Collections.swap(localItems, fromPos, toPos)
                adapter.notifyItemMoved(fromPos, toPos)
                return true
            }

            override fun onSwiped(viewHolder: RecyclerView.ViewHolder, direction: Int) {}
            override fun isLongPressDragEnabled(): Boolean = true
            override fun clearView(recyclerView: RecyclerView, viewHolder: RecyclerView.ViewHolder) {
                super.clearView(recyclerView, viewHolder)
                saveItems()
            }
        }
        ItemTouchHelper(callback).attachToRecyclerView(recyclerView)
    }

    inner class WidgetEditAdapter : RecyclerView.Adapter<WidgetEditAdapter.ViewHolder>() {

        inner class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
            val tvName: TextView = view.findViewById(1)
            val btnRemove: ImageView = view.findViewById(2)
            val dragHandle: ImageView = view.findViewById(3)
            
            // Size editors
            val tvCols: TextView = view.findViewById(4)
            val btnColMinus: Button = view.findViewById(5)
            val btnColPlus: Button = view.findViewById(6)
            
            val tvRows: TextView = view.findViewById(7)
            val btnRowMinus: Button = view.findViewById(8)
            val btnRowPlus: Button = view.findViewById(9)
        }

        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
            val layout = LinearLayout(context).apply {
                orientation = LinearLayout.VERTICAL
                layoutParams = RecyclerView.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT).apply { setMargins(0, 0, 0, 16) }
                setPadding(16, 16, 16, 16)
                setBackgroundColor(Color.parseColor("#33FFFFFF"))
            }
            
            val topRow = LinearLayout(context).apply {
                orientation = LinearLayout.HORIZONTAL
                layoutParams = LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT)
                gravity = Gravity.CENTER_VERTICAL
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
                textSize = 16f
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
            
            topRow.addView(dragHandle)
            topRow.addView(tvName)
            topRow.addView(btnRemove)
            layout.addView(topRow)
            
            // Editors Row
            val editorsRow = LinearLayout(context).apply {
                orientation = LinearLayout.HORIZONTAL
                layoutParams = LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT)
                gravity = Gravity.CENTER_VERTICAL
                setPadding(16, 16, 16, 0)
            }
            
            // Cols Editor
            val colsLayout = LinearLayout(context).apply {
                orientation = LinearLayout.HORIZONTAL
                layoutParams = LinearLayout.LayoutParams(0, LayoutParams.WRAP_CONTENT, 1f)
                gravity = Gravity.CENTER_VERTICAL
            }
            colsLayout.addView(TextView(context).apply { text = "Cols: "; setTextColor(Color.LTGRAY) })
            
            val btnColMinus = Button(context).apply { id = 5; text = "-"; textSize = 10f; layoutParams = LinearLayout.LayoutParams(100, 100) }
            val tvCols = TextView(context).apply { id = 4; setTextColor(Color.WHITE); setPadding(16, 0, 16, 0) }
            val btnColPlus = Button(context).apply { id = 6; text = "+"; textSize = 10f; layoutParams = LinearLayout.LayoutParams(100, 100) }
            
            colsLayout.addView(btnColMinus)
            colsLayout.addView(tvCols)
            colsLayout.addView(btnColPlus)
            
            // Rows Editor
            val rowsLayout = LinearLayout(context).apply {
                orientation = LinearLayout.HORIZONTAL
                layoutParams = LinearLayout.LayoutParams(0, LayoutParams.WRAP_CONTENT, 1f)
                gravity = Gravity.CENTER_VERTICAL
            }
            rowsLayout.addView(TextView(context).apply { text = "Rows: "; setTextColor(Color.LTGRAY) })
            
            val btnRowMinus = Button(context).apply { id = 8; text = "-"; textSize = 10f; layoutParams = LinearLayout.LayoutParams(100, 100) }
            val tvRows = TextView(context).apply { id = 7; setTextColor(Color.WHITE); setPadding(16, 0, 16, 0) }
            val btnRowPlus = Button(context).apply { id = 9; text = "+"; textSize = 10f; layoutParams = LinearLayout.LayoutParams(100, 100) }
            
            rowsLayout.addView(btnRowMinus)
            rowsLayout.addView(tvRows)
            rowsLayout.addView(btnRowPlus)
            
            editorsRow.addView(colsLayout)
            editorsRow.addView(rowsLayout)
            layout.addView(editorsRow)

            return ViewHolder(layout)
        }

        override fun onBindViewHolder(holder: ViewHolder, position: Int) {
            val item = localItems[position]
            val info = appWidgetManager.getAppWidgetInfo(item.id)
            
            holder.tvName.text = info?.loadLabel(context.packageManager) ?: "Widget ${item.id} (Unknown)"
            
            holder.tvCols.text = item.cols.toString()
            holder.tvRows.text = item.rows.toString()
            
            holder.btnColMinus.setOnClickListener {
                if (item.cols > 1) {
                    item.cols--
                    holder.tvCols.text = item.cols.toString()
                    saveItems()
                }
            }
            holder.btnColPlus.setOnClickListener {
                item.cols++
                holder.tvCols.text = item.cols.toString()
                saveItems()
            }
            
            holder.btnRowMinus.setOnClickListener {
                if (item.rows > 1) {
                    item.rows--
                    holder.tvRows.text = item.rows.toString()
                    saveItems()
                }
            }
            holder.btnRowPlus.setOnClickListener {
                item.rows++
                holder.tvRows.text = item.rows.toString()
                saveItems()
            }
            
            holder.btnRemove.setOnClickListener {
                val pos = holder.adapterPosition
                if (pos != RecyclerView.NO_POSITION) {
                    val removed = localItems.removeAt(pos)
                    notifyItemRemoved(pos)
                    saveItems()
                    
                    try {
                        AppWidgetHelper.getHost(context).deleteAppWidgetId(removed.id)
                    } catch (e: Exception) {}
                }
            }
        }

        override fun getItemCount(): Int = localItems.size
    }
}
"""

with open('app/src/main/java/com/example/service/WidgetsGridEditOverlayView.kt', 'w') as f:
    f.write(new_content)

