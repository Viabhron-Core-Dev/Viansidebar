package com.example.service

import android.annotation.SuppressLint
import android.content.Context
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
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.ItemTouchHelper
import androidx.recyclerview.widget.RecyclerView
import org.json.JSONArray
import com.example.R
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

@SuppressLint("ViewConstructor")
class SidebarEditOverlayView(
    context: Context,
    private val manager: SidebarAppsManager,
    private val windowManager: WindowManager,
    private val serviceScope: CoroutineScope,
    private val onAddClicked: () -> Unit,
    private val onClose: () -> Unit
) : FrameLayout(context) {

    private val layoutParams: WindowManager.LayoutParams
    private val recyclerView: RecyclerView
    private val adapter: EditAdapter
    private val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)

    // Local mutable list of IDs representing the current edit state
    val localIds = mutableListOf<String>()
    val rootLocalIds = mutableListOf<String>()
    var currentFolderId: String? = null
    var titleView: TextView? = null
    var btnBack: Button? = null
    var btnReset: Button? = null

    init {
        com.example.LogKeeper.writeLog("SidebarEdit", "Opened sidebar edit overlay")
        val windowType = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        } else {
            @Suppress("DEPRECATION")
            WindowManager.LayoutParams.TYPE_PHONE
        }

        layoutParams = WindowManager.LayoutParams(
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.MATCH_PARENT,
            windowType,
            WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL or WindowManager.LayoutParams.FLAG_WATCH_OUTSIDE_TOUCH,
            PixelFormat.TRANSLUCENT
        )

        setBackgroundColor(Color.parseColor("#E6000000")) // Semi-transparent black

        // Initialize local list with current items
        localIds.addAll(manager.activeItems.map { it.id })
            com.example.LogKeeper.writeLog("SidebarEdit", "localIds on attach: $localIds")

        val rootLayout = LinearLayout(context).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            layoutParams = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        }

        // Top Buttons Row
        val buttonsLayout = LinearLayout(context).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            layoutParams = LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT).apply {
                setMargins(0, 0, 0, 40)
            }
        }

        titleView = TextView(context).apply {
            text = "Edit Sidebar"
            setTextColor(Color.WHITE)
            textSize = 20f
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, 16)
        }
        rootLayout.addView(titleView)

        val btnAdd = Button(context).apply {
            text = "Add"
            setOnClickListener { 
                com.example.LogKeeper.writeLog("SidebarEdit", "Add button clicked")
                onAddClicked() 
            }
        }
        btnReset = Button(context).apply {
            text = "Empty"
            setOnClickListener {
                localIds.clear()
                refresh()
            }
        }
        btnBack = Button(context).apply {
            text = "Back"
            visibility = View.GONE
            setOnClickListener { exitFolder() }
        }
        val btnSave = Button(context).apply {
            text = "Save"
            setOnClickListener { saveAndClose() }
        }
        val btnCancel = Button(context).apply {
            text = "Cancel"
            setOnClickListener { close() }
        }

        buttonsLayout.addView(btnAdd)
        buttonsLayout.addView(btnReset!!)
        buttonsLayout.addView(btnBack!!)
        buttonsLayout.addView(btnSave)
        buttonsLayout.addView(btnCancel)

        rootLayout.addView(buttonsLayout)

        // Sidebar-like window in the middle
        val density = context.resources.displayMetrics.density
        val sidebarWidth = (prefs.getInt("sidebar_width", 180) * density).toInt()
        val sidebarHeight = (prefs.getInt("sidebar_height", 450) * density).toInt()
        
        val sidebarContainer = FrameLayout(context).apply {
            layoutParams = LinearLayout.LayoutParams(sidebarWidth, sidebarHeight)
            val shape = android.graphics.drawable.GradientDrawable()
            shape.shape = android.graphics.drawable.GradientDrawable.RECTANGLE
            shape.cornerRadius = 20f * density
            val opacity = prefs.getFloat("sidebar_transparency", 0.9f)
            val alphaInt = (opacity * 255).toInt().coerceIn(0, 255)
            shape.setColor(Color.argb(alphaInt, 0, 0, 0))
            background = shape
            setPadding(10, 10, 10, 10)
        }

        val columns = prefs.getInt("sidebar_columns", 3)
        recyclerView = RecyclerView(context).apply {
            layoutParams = FrameLayout.LayoutParams(FrameLayout.LayoutParams.MATCH_PARENT, FrameLayout.LayoutParams.MATCH_PARENT)
            layoutManager = GridLayoutManager(context, columns).apply {
                spanSizeLookup = object : GridLayoutManager.SpanSizeLookup() {
                    override fun getSpanSize(position: Int): Int {
                        val id = localIds[position]
                        val item = manager.parseId(id)
                        return if (item is SidebarItem.Spacer) columns else 1
                    }
                }
            }
        }

        adapter = EditAdapter()
        recyclerView.adapter = adapter
        sidebarContainer.addView(recyclerView)

        val touchHelperCallback = object : ItemTouchHelper.SimpleCallback(
            ItemTouchHelper.UP or ItemTouchHelper.DOWN or ItemTouchHelper.LEFT or ItemTouchHelper.RIGHT,
            0
        ) {
            override fun onMove(
                recyclerView: RecyclerView,
                viewHolder: RecyclerView.ViewHolder,
                target: RecyclerView.ViewHolder
            ): Boolean {
                val from = viewHolder.adapterPosition
                val to = target.adapterPosition
                val item = localIds.removeAt(from)
                localIds.add(to, item)
                adapter.notifyItemMoved(from, to)
                return true
            }

            override fun onSwiped(viewHolder: RecyclerView.ViewHolder, direction: Int) {}
            
            override fun clearView(recyclerView: RecyclerView, viewHolder: RecyclerView.ViewHolder) {
                super.clearView(recyclerView, viewHolder)
                com.example.LogKeeper.writeLog("SidebarEdit", "Item moved to position: ${viewHolder.adapterPosition}")
            }
        }
        val itemTouchHelper = ItemTouchHelper(touchHelperCallback)
        itemTouchHelper.attachToRecyclerView(recyclerView)

        rootLayout.addView(sidebarContainer)
        addView(rootLayout)
    }

    fun refresh() {
        adapter.notifyDataSetChanged()
    }

    fun attach() {
        if (windowToken == null) {
            rootLocalIds.clear()
            rootLocalIds.addAll(manager.activeItems.map { it.id })
            currentFolderId = null
            localIds.clear()
            localIds.addAll(rootLocalIds)
            com.example.LogKeeper.writeLog("SidebarEdit", "localIds on attach: $localIds")
            updateUIState()
            windowManager.addView(this, layoutParams)
        }
    }

    fun detach() {
        if (windowToken != null) {
            windowManager.removeView(this)
        }
    }

    private fun close() {
        onClose()
    }

    private fun commitCurrentFolder() {
        val folderId = currentFolderId ?: return
        val uuid = folderId.split(":")[1]
        val index = rootLocalIds.indexOfFirst { it.startsWith("folder:$uuid:") }
        if (index != -1) {
            val oldStr = rootLocalIds[index]
            val parts = oldStr.split(":", limit = 3)
            val folderDataStr = parts[2]
            val obj = org.json.JSONObject(folderDataStr)
            val itemsArr = JSONArray()
            localIds.forEach { itemsArr.put(it) }
            obj.put("items", itemsArr)
            rootLocalIds[index] = "folder:${parts[1]}:${obj.toString()}"
        }
    }

    fun saveCurrentState() {
        com.example.LogKeeper.writeLog("SidebarEdit", "Saving current state. isFolder=${currentFolderId != null}")
        if (currentFolderId != null) {
            commitCurrentFolder()
        } else {
            rootLocalIds.clear()
            rootLocalIds.addAll(localIds)
        }
        val jArr = JSONArray()
        rootLocalIds.forEach { jArr.put(it) }
        prefs.edit().putString("sidebar_apps", jArr.toString()).apply()
        manager.reloadActiveApps()
    }

    private fun enterFolder(folder: SidebarItem.Folder) {
        com.example.LogKeeper.writeLog("SidebarEdit", "Entering folder: ${folder.name}")
        rootLocalIds.clear()
        rootLocalIds.addAll(localIds) // Save current root state
        currentFolderId = folder.id
        localIds.clear()
        localIds.addAll(folder.items)
        updateUIState()
    }

    private fun exitFolder() {
        com.example.LogKeeper.writeLog("SidebarEdit", "Exiting folder")
        commitCurrentFolder()
        currentFolderId = null
        localIds.clear()
        localIds.addAll(rootLocalIds)
        updateUIState()
    }

    private fun updateUIState() {
        if (currentFolderId != null) {
            val f = manager.parseId(currentFolderId!!) as? SidebarItem.Folder
            titleView?.text = "Editing Folder: ${f?.name ?: ""}"
            btnBack?.visibility = View.VISIBLE
            btnReset?.visibility = View.GONE
        } else {
            titleView?.text = "Edit Sidebar"
            btnBack?.visibility = View.GONE
            btnReset?.visibility = View.VISIBLE
        }
        refresh()
    }

    private fun saveAndClose() {
        saveCurrentState()
        close()
    }

    private inner class EditViewHolder(val view: LinearLayout) : RecyclerView.ViewHolder(view) {
        val icon = ImageView(context)
        val label = TextView(context)
        init {
            view.orientation = LinearLayout.VERTICAL
            view.gravity = Gravity.CENTER
            val density = context.resources.displayMetrics.density
            val size = (48 * density).toInt()
            
            icon.layoutParams = LinearLayout.LayoutParams(size, size)
            icon.scaleType = ImageView.ScaleType.FIT_CENTER
            
            label.setTextColor(Color.WHITE)
            label.textSize = 10f
            label.gravity = Gravity.CENTER
            label.maxLines = 2
            label.setPadding(0, 8, 0, 0)
            
            view.addView(icon)
            view.addView(label)
            
            view.layoutParams = ViewGroup.MarginLayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT).apply {
                setMargins(0, 16, 0, 16)
            }
        }
    }

    private inner class EditAdapter : RecyclerView.Adapter<EditViewHolder>() {
        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): EditViewHolder {
            return EditViewHolder(LinearLayout(context))
        }

        override fun onBindViewHolder(holder: EditViewHolder, position: Int) {
            val id = localIds[position]
            val item = manager.parseId(id)
            
            if (item == null) {
                holder.label.text = "Unknown"
                holder.icon.setImageResource(android.R.drawable.ic_dialog_alert)
                return
            }
            
            holder.label.text = item.label

            if (item is SidebarItem.App) {
                val cached = manager.getIconBitmap(item.id)
                if (cached != null) {
                    holder.icon.setBackgroundColor(Color.TRANSPARENT)
                    holder.icon.setImageBitmap(cached)
                } else {
                    serviceScope.launch {
                        val bitmap = manager.loadIcon(item.packageName)
                        if (bitmap != null) {
                            withContext(Dispatchers.Main) {
                                holder.icon.setBackgroundColor(Color.TRANSPARENT)
                                holder.icon.setImageBitmap(bitmap)
                            }
                        } else {
                            withContext(Dispatchers.Main) {
                                holder.icon.setImageResource(android.R.mipmap.sym_def_app_icon)
                            }
                        }
                    }
                }
            } else if (item is SidebarItem.IntentAction) {
                val pkg = item.componentStr.split("/").getOrNull(0) ?: ""
                val cached = manager.getIconBitmap(item.id)
                if (cached != null) {
                    holder.icon.setBackgroundColor(Color.TRANSPARENT)
                    holder.icon.setImageBitmap(cached)
                } else {
                    serviceScope.launch {
                        val bitmap = manager.loadIcon(pkg)
                        if (bitmap != null) {
                            withContext(Dispatchers.Main) {
                                holder.icon.setBackgroundColor(Color.TRANSPARENT)
                                holder.icon.setImageBitmap(bitmap)
                            }
                        } else {
                            withContext(Dispatchers.Main) {
                                holder.icon.setImageResource(android.R.mipmap.sym_def_app_icon)
                            }
                        }
                    }
                }
            } else if (item is SidebarItem.SystemAction || item is SidebarItem.VolumeAction || item is SidebarItem.MediaAction || item is SidebarItem.DisplayAction || item is SidebarItem.SettingsShortcut || item is SidebarItem.QuickTile) {
                val resId = when (item) {
                    is SidebarItem.SystemAction -> item.iconResId
                    is SidebarItem.VolumeAction -> item.iconResId
                    is SidebarItem.MediaAction -> item.iconResId
                    is SidebarItem.SettingsShortcut -> item.iconResId
                    is SidebarItem.DisplayAction -> item.iconResId
                    is SidebarItem.QuickTile -> item.iconResId
                    else -> 0
                }
                holder.icon.setImageResource(resId)
                holder.icon.setColorFilter(Color.WHITE)
            } else if (item is SidebarItem.Folder) {
                val cHex = try { Color.parseColor(item.colorHex) } catch(e:Exception){ Color.parseColor("#00BFA5") }
                val iconC = Color.WHITE
                val miniIcons = item.items.take(9).mapNotNull { manager.getIconBitmap(it) }
                holder.icon.setImageDrawable(FolderStyleDrawable(item.folderStyle, cHex, iconC, miniIcons))
                
                if (miniIcons.size < minOf(item.items.size, 9)) {
                    serviceScope.launch {
                        var newlyLoaded = false
                        for (subItem in item.items.take(9)) {
                            if (manager.getIconBitmap(subItem) == null) {
                                val pkg = when {
                                    subItem.startsWith("app:") -> subItem.substringAfter("app:")
                                    subItem.startsWith("intent:") -> subItem.substringAfter("intent:").split("/").getOrNull(0) ?: ""
                                    else -> ""
                                }
                                if (pkg.isNotEmpty()) {
                                    val bitmap = manager.loadIcon(pkg)
                                    if (bitmap != null) {
                                        newlyLoaded = true
                                    }
                                }
                            }
                        }
                        if (newlyLoaded) {
                            withContext(Dispatchers.Main) {
                                adapter.notifyItemChanged(position)
                            }
                        }
                    }
                }
            } else if (item is SidebarItem.Link) {
                holder.icon.setImageResource(android.R.drawable.ic_menu_set_as)
                holder.icon.setColorFilter(Color.WHITE)
            } else if (item is SidebarItem.Spacer) {
                holder.icon.setImageResource(android.R.drawable.ic_menu_crop)
                holder.icon.setColorFilter(Color.GRAY)
            }
            
            holder.view.setOnClickListener {
                val actionList = mutableListOf("Change Icon", "Remove")
                if (item is SidebarItem.Folder) {
                    actionList.add(0, "Grid Size")
                    actionList.add(0, "Folder Style")
                    actionList.add(0, "Edit Contents")
                }
                var popupWindow: android.widget.PopupWindow? = null
                val popupLayout = LinearLayout(context).apply {
                    orientation = LinearLayout.VERTICAL
                    val shape = android.graphics.drawable.GradientDrawable()
                    shape.shape = android.graphics.drawable.GradientDrawable.RECTANGLE
                    shape.cornerRadius = 16f * context.resources.displayMetrics.density
                    shape.setColor(Color.WHITE)
                    shape.setStroke(1, Color.LTGRAY)
                    background = shape
                }

                actionList.forEach { action ->
                    val actionView = TextView(context).apply {
                        text = action
                        val pad = (12 * context.resources.displayMetrics.density).toInt()
                        val padH = (16 * context.resources.displayMetrics.density).toInt()
                        setPadding(padH, pad, padH, pad)
                        setTextColor(android.graphics.Color.BLACK)
                        textSize = 14f
                        val outValue = android.util.TypedValue()
                        context.theme.resolveAttribute(android.R.attr.selectableItemBackground, outValue, true)
                        setBackgroundResource(outValue.resourceId)
                        
                        setOnClickListener {
                            popupWindow?.dismiss()
                            when (action) {
                                "Edit Contents" -> {
                                    if (item is SidebarItem.Folder) {
                                        enterFolder(item)
                                    }
                                }
                                "Remove" -> {
                                    com.example.LogKeeper.writeLog("SidebarEdit", "Removed item: ${item.label}")
                                    localIds.removeAt(holder.adapterPosition)
                                    refresh()
                                }
                                "Folder Style" -> {
                                    com.example.LogKeeper.writeLog("SidebarEdit", "Editing folder style for ${item.label}")
                                    if (item is SidebarItem.Folder) {
                                        showFolderStyleDialog(context, item, manager) { styleIndex, popupCols ->
                                            val json = org.json.JSONObject().apply {
                                                put("name", item.name)
                                                put("colorHex", item.colorHex)
                                                val jArr = org.json.JSONArray()
                                                item.items.forEach { jArr.put(it) }
                                                put("items", jArr)
                                                put("folderStyle", styleIndex)
                                                put("popupColumns", popupCols)
                                                put("popupRows", item.popupRows)
                                            }
                                            val newId = "folder:${item.uuid}:$json"
                                            val pos = localIds.indexOf(item.id)
                                            if (pos != -1) {
                                                localIds[pos] = newId
                                                refresh()
                                            }
                                        }
                                    }
                                }
                                "Grid Size" -> {
                                    com.example.LogKeeper.writeLog("SidebarEdit", "Editing grid size for ${item.label}")
                                    if (item is SidebarItem.Folder) {
                                        showGridSizeDialog(context, item, manager) { cols, rows ->
                                            val json = org.json.JSONObject().apply {
                                                put("name", item.name)
                                                put("colorHex", item.colorHex)
                                                val jArr = org.json.JSONArray()
                                                item.items.forEach { jArr.put(it) }
                                                put("items", jArr)
                                                put("folderStyle", item.folderStyle)
                                                put("popupColumns", cols)
                                                put("popupRows", rows)
                                            }
                                            val newId = "folder:${item.uuid}:$json"
                                            val pos = localIds.indexOf(item.id)
                                            if (pos != -1) {
                                                localIds[pos] = newId
                                                refresh()
                                            }
                                        }
                                    }
                                }
                                "Change Icon" -> {
                                    val et = android.widget.EditText(context).apply {
                                        hint = "Emoji or App Package"
                                        val current = prefs.getString("custom_icon_${item.id}", "")
                                        setText(current)
                                    }
                                    val dialog = android.app.AlertDialog.Builder(context, android.R.style.Theme_DeviceDefault_Light_Dialog_Alert)
                                        .setTitle("Edit Icon")
                                        .setView(et)
                                        .setPositiveButton("Save") { _, _ ->
                                            val input = et.text.toString().trim()
                                            if (input.isEmpty()) {
                                                prefs.edit().remove("custom_icon_${item.id}").apply()
                                            } else {
                                                prefs.edit().putString("custom_icon_${item.id}", input).apply()
                                            }
                                            refresh()
                                        }
                                        .setNegativeButton("Cancel", null)
                                        .create()
                                    dialog.window?.setType(if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY else WindowManager.LayoutParams.TYPE_PHONE)
                                    dialog.show()
                                }
                            }
                        }
                    }
                    popupLayout.addView(actionView)
                }

                popupWindow = android.widget.PopupWindow(
                    popupLayout,
                    ViewGroup.LayoutParams.WRAP_CONTENT,
                    ViewGroup.LayoutParams.WRAP_CONTENT,
                    true
                )
                popupWindow.elevation = 10f * context.resources.displayMetrics.density
                popupWindow.showAsDropDown(holder.view, 0, 0)
            }
        }
        override fun getItemCount(): Int = localIds.size
    }
}

private fun showGridSizeDialog(
    context: Context,
    item: SidebarItem.Folder,
    manager: SidebarAppsManager,
    onGridSizeSelected: (Int, Int) -> Unit
) {
    val layout = LinearLayout(context).apply {
        orientation = LinearLayout.VERTICAL
        setPadding(40, 40, 40, 40)
        setBackgroundColor(android.graphics.Color.WHITE)
    }

    val title = TextView(context).apply {
        text = "Popup Grid Size"
        textSize = 18f
        typeface = android.graphics.Typeface.DEFAULT_BOLD
        setTextColor(android.graphics.Color.BLACK)
        setPadding(0, 0, 0, 20)
    }
    layout.addView(title)
    
    val desc = TextView(context).apply {
        text = "0 = auto calculate based on items"
        textSize = 12f
        setTextColor(android.graphics.Color.DKGRAY)
        setPadding(0, 0, 0, 20)
    }
    layout.addView(desc)

    val rowColContainer = LinearLayout(context).apply {
        orientation = LinearLayout.HORIZONTAL
        gravity = Gravity.CENTER
    }
    layout.addView(rowColContainer)

    var currentCols = item.popupColumns
    var currentRows = item.popupRows

    // Function to create a spinner-like column/row picker
    fun createPicker(label: String, initialValue: Int, onValueChanged: (Int) -> Unit): LinearLayout {
        val picker = LinearLayout(context).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            setPadding(20, 0, 20, 0)
        }
        val labelView = TextView(context).apply {
            text = label
            textSize = 14f
            setTextColor(android.graphics.Color.BLACK)
            gravity = Gravity.CENTER
        }
        picker.addView(labelView)

        val btnUp = android.widget.ImageButton(context).apply {
            setImageResource(android.R.drawable.arrow_up_float)
            setBackgroundColor(android.graphics.Color.TRANSPARENT)
            setColorFilter(android.graphics.Color.DKGRAY)
        }
        picker.addView(btnUp)

        val valueView = TextView(context).apply {
            text = initialValue.toString()
            textSize = 24f
            typeface = android.graphics.Typeface.DEFAULT_BOLD
            setTextColor(android.graphics.Color.BLACK)
            gravity = Gravity.CENTER
        }
        picker.addView(valueView)

        val btnDown = android.widget.ImageButton(context).apply {
            setImageResource(android.R.drawable.arrow_down_float)
            setBackgroundColor(android.graphics.Color.TRANSPARENT)
            setColorFilter(android.graphics.Color.DKGRAY)
        }
        picker.addView(btnDown)

        var v = initialValue
        btnUp.setOnClickListener {
            v++
            valueView.text = v.toString()
            onValueChanged(v)
        }
        btnDown.setOnClickListener {
            if (v > 0) {
                v--
                valueView.text = v.toString()
                onValueChanged(v)
            }
        }
        return picker
    }

    rowColContainer.addView(createPicker("Columns", currentCols) { currentCols = it })
    rowColContainer.addView(createPicker("Rows", currentRows) { currentRows = it })

    val dialog = android.app.AlertDialog.Builder(context)
        .setView(layout)
        .setPositiveButton("Save") { _, _ ->
            onGridSizeSelected(currentCols, currentRows)
        }
        .setNegativeButton("Cancel", null)
        .create()

    dialog.window?.setType(if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY else WindowManager.LayoutParams.TYPE_PHONE)
    dialog.show()
}
