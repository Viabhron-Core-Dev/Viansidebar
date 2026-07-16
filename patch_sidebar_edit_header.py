import re

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "r") as f:
    content = f.read()

target = """        val btnAdd = Button(this).apply {
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
        mainLayout.addView(headerLayout)"""

replacement = """        val buttonsLayout = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            layoutParams = LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)
            gravity = Gravity.CENTER_VERTICAL
        }

        fun createSmallBtn(txt: String, onClick: () -> Unit): Button {
            return Button(this).apply {
                text = txt
                textSize = 10f
                setPadding(8, 0, 8, 0)
                layoutParams = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
                setOnClickListener { onClick() }
            }
        }

        val btnAdd = createSmallBtn("Add") {
            val intent = Intent(this@SidebarEditActivity, AddElementActivity::class.java)
            startActivityForResult(intent, 100)
        }
        val btnEmpty = createSmallBtn("Empty") {
            localIds.add("spacer:${System.currentTimeMillis()}:{\\"heightDp\\":56}")
            adapter.notifyItemInserted(localIds.size - 1)
        }
        val btnSave = createSmallBtn("Save") {
            saveIds()
            finish()
        }
        val btnCancel = createSmallBtn("Cancel") {
            finish()
        }
        
        buttonsLayout.addView(btnAdd)
        buttonsLayout.addView(btnEmpty)
        buttonsLayout.addView(btnSave)
        buttonsLayout.addView(btnCancel)
        
        val fullHeaderLayout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutParams = LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(0, 0, 0, 16)
        }
        fullHeaderLayout.addView(headerLayout)
        fullHeaderLayout.addView(buttonsLayout)
        mainLayout.addView(fullHeaderLayout)"""

content = content.replace(target, replacement)

# We also need to fix headerLayout so it doesn't take the full width and pushes the buttons down.
header_layout_target = """        // Header
        val headerLayout = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            layoutParams = LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)
            gravity = Gravity.CENTER_VERTICAL
            setPadding(0, 0, 0, 16)
        }"""
header_layout_replacement = """        // Header
        val headerLayout = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            layoutParams = LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)
            gravity = Gravity.CENTER_VERTICAL
            setPadding(0, 0, 0, 8)
        }"""
content = content.replace(header_layout_target, header_layout_replacement)

# Ensure rows show in both App Grid edit mode and Folder edit mode!
rows_target = """        if (folderUuid != null) {
            controlsLayout.addView(rowsLayout)
        }"""
rows_replacement = """        controlsLayout.addView(rowsLayout)"""
content = content.replace(rows_target, rows_replacement)

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "w") as f:
    f.write(content)
