import re

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'r') as f:
    content = f.read()

new_dialog_code = """
private fun showGridSizeDialog(
    context: Context,
    item: SidebarItem.Folder,
    manager: SidebarAppsManager,
    onGridSizeSelected: (Int) -> Unit
) {
    val layout = LinearLayout(context).apply {
        orientation = LinearLayout.VERTICAL
        setPadding(50, 40, 50, 40)
        setBackgroundColor(Color.WHITE)
    }

    val title = TextView(context).apply {
        text = "Popup Grid Size"
        textSize = 18f
        typeface = Typeface.DEFAULT_BOLD
        setTextColor(Color.BLACK)
        setPadding(0, 0, 0, 20)
    }
    layout.addView(title)
    
    val desc = TextView(context).apply {
        text = "Enter number of columns for this folder's popup (0 = default/auto)"
        textSize = 14f
        setTextColor(Color.DKGRAY)
        setPadding(0, 0, 0, 20)
    }
    layout.addView(desc)

    val colsInput = android.widget.EditText(context).apply {
        inputType = android.text.InputType.TYPE_CLASS_NUMBER
        setText(item.popupColumns.toString())
        setTextColor(Color.BLACK)
    }
    layout.addView(colsInput)

    val dialog = android.app.AlertDialog.Builder(context)
        .setView(layout)
        .setPositiveButton("Save") { _, _ ->
            val colsStr = colsInput.text.toString()
            val cols = if (colsStr.isNotEmpty()) colsStr.toInt() else 0
            
            val json = org.json.JSONObject().apply {
                put("name", item.name)
                put("colorHex", item.colorHex)
                val jArr = org.json.JSONArray()
                item.items.forEach { jArr.put(it) }
                put("items", jArr)
                put("folderStyle", item.folderStyle)
                put("popupColumns", cols)
            }
            manager.removeItem(item.id)
            manager.addItem("folder:${item.uuid}:$json")
            
            onGridSizeSelected(cols)
        }
        .setNegativeButton("Cancel", null)
        .create()

    dialog.window?.setType(if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) android.view.WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY else android.view.WindowManager.LayoutParams.TYPE_PHONE)
    dialog.show()
}
"""

if "private fun showGridSizeDialog" not in content:
    content = content + new_dialog_code
    with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'w') as f:
        f.write(content)
