package com.example

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.FrameLayout
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import androidx.activity.ComponentActivity
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.ItemTouchHelper
import androidx.recyclerview.widget.RecyclerView
import com.example.service.SidebarAppsManager
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray
import java.util.Collections

class SidebarEditActivity : ComponentActivity() {

    private lateinit var recyclerView: RecyclerView
    private lateinit var adapter: EditAdapter
    private lateinit var prefs: android.content.SharedPreferences
    val localIds = mutableListOf<String>()
    private var folderUuid: String? = null
    private var folderName: String = "Folder"
    private var folderColor: String = "#444444"
    private var folderStyle: Int = 0
    private var totalCols = 3
    private var totalRows = 3

    
    private lateinit var manager: SidebarAppsManager
    private val serviceScope = CoroutineScope(Dispatchers.IO)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        prefs = getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
        manager = SidebarAppsManager(this, prefs, serviceScope) {}
        
        folderUuid = intent.getStringExtra("FOLDER_UUID")
        loadLocalIds()

        if (folderUuid == null) {
            totalCols = prefs.getInt("sidebar_columns", 3)
        }

        val mainLayout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutParams = ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
            setPadding(32, 32, 32, 32)
            gravity = Gravity.CENTER_HORIZONTAL
            setBackgroundColor(Color.BLACK)
        }

        // Header
        val headerLayout = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            layoutParams = LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)
            gravity = Gravity.CENTER_VERTICAL
            setPadding(0, 0, 0, 16)
        }

        val controlsLayout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutParams = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
            gravity = Gravity.CENTER_VERTICAL
        }
        val colsLayout = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }
        colsLayout.addView(TextView(this).apply { text = "Cols: "; setTextColor(Color.LTGRAY) })
        val btnColMinus = Button(this).apply { text = "-"; layoutParams = LinearLayout.LayoutParams(100, 100); setOnClickListener { if (totalCols > 1) { totalCols--; updateColsDisplay(); updateGrid() } } }
        val tvCols = TextView(this).apply { id = 101; setTextColor(Color.WHITE); setPadding(16, 0, 16, 0); text = totalCols.toString() }
        val btnColPlus = Button(this).apply { text = "+"; layoutParams = LinearLayout.LayoutParams(100, 100); setOnClickListener { totalCols++; updateColsDisplay(); updateGrid() } }
        colsLayout.addView(btnColMinus); colsLayout.addView(tvCols); colsLayout.addView(btnColPlus)
        controlsLayout.addView(colsLayout)
        
        val rowsLayout = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }
        rowsLayout.addView(TextView(this).apply { text = "Rows: "; setTextColor(Color.LTGRAY) })
        val btnRowMinus = Button(this).apply { text = "-"; layoutParams = LinearLayout.LayoutParams(100, 100); setOnClickListener { if (totalRows > 1) { totalRows--; updateRowsDisplay() } } }
        val tvRows = TextView(this).apply { id = 102; setTextColor(Color.WHITE); setPadding(16, 0, 16, 0); text = totalRows.toString() }
        val btnRowPlus = Button(this).apply { text = "+"; layoutParams = LinearLayout.LayoutParams(100, 100); setOnClickListener { totalRows++; updateRowsDisplay() } }
        rowsLayout.addView(btnRowMinus); rowsLayout.addView(tvRows); rowsLayout.addView(btnRowPlus)
        if (folderUuid != null) {
            controlsLayout.addView(rowsLayout)
        }
        headerLayout.addView(controlsLayout)

        val btnAdd = Button(this).apply {
            text = "Add"
            setOnClickListener {
                val intent = Intent(this@SidebarEditActivity, AddElementActivity::class.java)
                startActivityForResult(intent, 100)
            }
        }

        val btnEmpty = Button(this).apply {
            text = "Empty"
            setOnClickListener {
                localIds.add("spacer:${System.currentTimeMillis()}:{\"heightDp\":56}")
                adapter.notifyItemInserted(localIds.size - 1)
            }
        }
        
        val btnSave = Button(this).apply {
            text = "Save"
            setOnClickListener {
                saveIds()
                finish()
            }
        }

        val btnCancel = Button(this).apply {
            text = "Cancel"
            setOnClickListener {
                finish()
            }
        }
        
        headerLayout.addView(btnAdd)
        headerLayout.addView(btnEmpty)
        headerLayout.addView(btnSave)
        headerLayout.addView(btnCancel)
        mainLayout.addView(headerLayout)


        adapter = EditAdapter()
        recyclerView = RecyclerView(this).apply {
            layoutParams = LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f)
            layoutManager = GridLayoutManager(this@SidebarEditActivity, totalCols)
            this.adapter = this@SidebarEditActivity.adapter
        }
        mainLayout.addView(recyclerView)

        setContentView(mainLayout)
        setupItemTouchHelper()
    }
    
    private fun updateColsDisplay() {
        findViewById<TextView>(101)?.text = totalCols.toString()
    }
    private fun updateRowsDisplay() {
        findViewById<TextView>(102)?.text = totalRows.toString()
    }
    private fun updateGrid() {
        if (::recyclerView.isInitialized) {
            recyclerView.layoutManager = GridLayoutManager(this, totalCols)
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 100 && resultCode == RESULT_OK) {
            val id = data?.getStringExtra("ELEMENT_ID")
            if (id != null) {
                localIds.add(id)
                adapter.notifyItemInserted(localIds.size - 1)
            }
        }
    }

    private fun loadLocalIds() {
        localIds.clear()
        val jsonStr = prefs.getString("sidebar_apps", """["system:log_keeper", "system:ebook_reader"]""") ?: """["system:log_keeper", "system:ebook_reader"]"""
        val arr = JSONArray(jsonStr)
        
        if (folderUuid != null) {
            for (i in 0 until arr.length()) {
                var item = arr.getString(i)
                if (item.startsWith("folder:$folderUuid:")) {
                    try {
                        val parts = item.split(":", limit = 3)
                        val folderDataStr = parts[2]
                        val obj = org.json.JSONObject(folderDataStr)
                        folderName = obj.optString("name", "Folder")
                        folderColor = obj.optString("colorHex", "#444444")
                        folderStyle = obj.optInt("folderStyle", 0)
                        totalCols = obj.optInt("popupColumns", 0)
                        if (totalCols <= 0) totalCols = prefs.getInt("sidebar_columns", 3)
                        totalRows = obj.optInt("popupRows", 0)
                        
                        val itemsArr = obj.optJSONArray("items") ?: org.json.JSONArray()
                        for (j in 0 until itemsArr.length()) {
                            localIds.add(itemsArr.getString(j))
                        }
                    } catch (e: Exception) {}
                    break
                }
            }
        } else {
            for (i in 0 until arr.length()) {
                localIds.add(arr.getString(i))
            }
        }
    }

    private fun saveIds() {
        val arr = JSONArray()
        localIds.forEach { arr.put(it) }
        
        if (folderUuid != null) {
            val jsonStr = prefs.getString("sidebar_apps", """["system:log_keeper", "system:ebook_reader"]""") ?: return
            val mainArr = JSONArray(jsonStr)
            val newMainArr = JSONArray()
            for (i in 0 until mainArr.length()) {
                var item = mainArr.getString(i)
                if (item.startsWith("folder:$folderUuid:")) {
                    val obj = org.json.JSONObject()
                    obj.put("name", folderName)
                    obj.put("colorHex", folderColor)
                    obj.put("folderStyle", folderStyle)
                    obj.put("popupColumns", totalCols)
                    obj.put("popupRows", totalRows)
                    obj.put("items", arr)
                    item = "folder:$folderUuid:${obj.toString()}"
                }
                newMainArr.put(item)
            }
            prefs.edit().putString("sidebar_apps", newMainArr.toString()).apply()
            com.example.LogKeeper.writeLog("SidebarEdit", "Saved ${localIds.size} items to folder $folderUuid.")
        } else {
            prefs.edit().putString("sidebar_apps", arr.toString()).apply()
            prefs.edit().putInt("sidebar_columns", totalCols).apply()
            com.example.LogKeeper.writeLog("SidebarEdit", "Saved ${localIds.size} items to apps grid.")
        }
        
        val updateIntent = Intent(this, com.example.service.FloatingReaderService::class.java).apply {
            action = "UPDATE_CONFIG"
        }
        startService(updateIntent)
    }

    private fun setupItemTouchHelper() {
        val callback = object : ItemTouchHelper.SimpleCallback(
            ItemTouchHelper.UP or ItemTouchHelper.DOWN or ItemTouchHelper.LEFT or ItemTouchHelper.RIGHT,
            0
        ) {
            override fun onMove(
                recyclerView: RecyclerView,
                viewHolder: RecyclerView.ViewHolder,
                target: RecyclerView.ViewHolder
            ): Boolean {
                val fromPos = viewHolder.bindingAdapterPosition
                val toPos = target.bindingAdapterPosition
                if (fromPos == RecyclerView.NO_POSITION || toPos == RecyclerView.NO_POSITION) return false
                Collections.swap(localIds, fromPos, toPos)
                adapter.notifyItemMoved(fromPos, toPos)
                return true
            }

            override fun onSwiped(viewHolder: RecyclerView.ViewHolder, direction: Int) {}
            override fun isLongPressDragEnabled(): Boolean = true
        }
        ItemTouchHelper(callback).attachToRecyclerView(recyclerView)
    }

    inner class EditAdapter : RecyclerView.Adapter<EditAdapter.ViewHolder>() {

        inner class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
            val iconView: ImageView = view.findViewById(1)
            val nameView: TextView = view.findViewById(2)
            val btnRemove: ImageView = view.findViewById(3)
        }

        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
            val density = resources.displayMetrics.density
            val layout = FrameLayout(this@SidebarEditActivity).apply {
                layoutParams = ViewGroup.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    (72 * density).toInt()
                )
                setPadding((4 * density).toInt(), (4 * density).toInt(), (4 * density).toInt(), (4 * density).toInt())
            }
            
            val contentLayout = LinearLayout(this@SidebarEditActivity).apply {
                orientation = LinearLayout.VERTICAL
                layoutParams = FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
                gravity = Gravity.CENTER
                setBackgroundColor(Color.parseColor("#33FFFFFF"))
            }

            val iconView = ImageView(this@SidebarEditActivity).apply {
                id = 1
                layoutParams = LinearLayout.LayoutParams((32 * density).toInt(), (32 * density).toInt())
                scaleType = ImageView.ScaleType.FIT_CENTER
            }

            val nameView = TextView(this@SidebarEditActivity).apply {
                id = 2
                setTextColor(Color.WHITE)
                textSize = 10f
                gravity = Gravity.CENTER
                layoutParams = LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT).apply {
                    topMargin = (4 * density).toInt()
                }
                maxLines = 1
            }

            contentLayout.addView(iconView)
            contentLayout.addView(nameView)
            
            val btnRemove = ImageView(this@SidebarEditActivity).apply {
                id = 3
                setImageResource(android.R.drawable.ic_menu_close_clear_cancel)
                layoutParams = FrameLayout.LayoutParams((24 * density).toInt(), (24 * density).toInt()).apply {
                    gravity = Gravity.TOP or Gravity.END
                }
                setColorFilter(Color.RED)
            }

            layout.addView(contentLayout)
            layout.addView(btnRemove)

            return ViewHolder(layout)
        }

        override fun onBindViewHolder(holder: ViewHolder, position: Int) {
            val id = localIds[position]
            
            if (id.startsWith("empty:")) {
                holder.iconView.setImageDrawable(null)
                holder.nameView.text = "Empty Space"
            } else {
                serviceScope.launch {
                    val item = manager.parseId(id)
                    val iconBitmap = manager.getIconBitmap(id)
                    withContext(Dispatchers.Main) {
                        if (item != null) {
                            holder.nameView.text = item.label
                        } else {
                            holder.nameView.text = "Unknown"
                        }
                        if (iconBitmap != null) {
                            holder.iconView.setImageBitmap(iconBitmap)
                        } else {
                            holder.iconView.setImageResource(android.R.drawable.sym_def_app_icon)
                            if (item is com.example.service.SidebarItem.App) {
                                val loaded = manager.loadIcon(item.packageName)
                                if (loaded != null) {
                                    holder.iconView.setImageBitmap(loaded)
                                }
                            } else if (item is com.example.service.SidebarItem.IntentAction) {
                                try {
                                    val uriStr = item.uri
                                    val pkg = android.content.Intent.parseUri(uriStr, android.content.Intent.URI_INTENT_SCHEME).`package` ?: android.content.Intent.parseUri(uriStr, android.content.Intent.URI_INTENT_SCHEME).component?.packageName ?: ""
                                    val loaded = manager.loadIcon(pkg)
                                    if (loaded != null) {
                                        holder.iconView.setImageBitmap(loaded)
                                    }
                                } catch (e: Exception) {}
                            }
                        }
                    }
                }
            }

            holder.itemView.setOnClickListener {
                if (id.startsWith("folder:")) {
                    val uuid = id.split(":")[1]
                    val intent = Intent(this@SidebarEditActivity, SidebarEditActivity::class.java).apply {
                        putExtra("FOLDER_UUID", uuid)
                    }
                    startActivity(intent)
                }
            }
            holder.btnRemove.setOnClickListener {
                val pos = holder.bindingAdapterPosition
                if (pos != RecyclerView.NO_POSITION) {
                    localIds.removeAt(pos)
                    notifyItemRemoved(pos)
                }
            }
        }

        override fun getItemCount(): Int = localIds.size
    }
}
