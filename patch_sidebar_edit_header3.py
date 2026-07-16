import re

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "r") as f:
    content = f.read()

target = """        // Header
        val headerLayout = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            layoutParams = LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)
            gravity = Gravity.CENTER_VERTICAL
            setPadding(0, 0, 0, 8)
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
        controlsLayout.addView(rowsLayout)
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
                localIds.add("spacer:${System.currentTimeMillis()}:{\\"heightDp\\":56}")
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

replacement = """        // Header
        val fullHeaderLayout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutParams = LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(0, 0, 0, 8)
        }

        val controlsLayout = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            layoutParams = LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)
            gravity = Gravity.CENTER_VERTICAL
            setPadding(0, 0, 0, 4)
        }
        
        val colsLayout = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            layoutParams = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
        }
        colsLayout.addView(TextView(this).apply { text = "Cols: "; textSize = 12f; setTextColor(Color.LTGRAY) })
        val btnColMinus = Button(this).apply { text = "-"; textSize = 14f; setPadding(0, 0, 0, 0); layoutParams = LinearLayout.LayoutParams(80, 80); setOnClickListener { if (totalCols > 1) { totalCols--; updateColsDisplay(); updateGrid() } } }
        val tvCols = TextView(this).apply { id = 101; setTextColor(Color.WHITE); textSize = 14f; setPadding(8, 0, 8, 0); text = totalCols.toString() }
        val btnColPlus = Button(this).apply { text = "+"; textSize = 14f; setPadding(0, 0, 0, 0); layoutParams = LinearLayout.LayoutParams(80, 80); setOnClickListener { totalCols++; updateColsDisplay(); updateGrid() } }
        colsLayout.addView(btnColMinus); colsLayout.addView(tvCols); colsLayout.addView(btnColPlus)
        controlsLayout.addView(colsLayout)
        
        val rowsLayout = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            layoutParams = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
        }
        rowsLayout.addView(TextView(this).apply { text = "Rows: "; textSize = 12f; setTextColor(Color.LTGRAY) })
        val btnRowMinus = Button(this).apply { text = "-"; textSize = 14f; setPadding(0, 0, 0, 0); layoutParams = LinearLayout.LayoutParams(80, 80); setOnClickListener { if (totalRows > 1) { totalRows--; updateRowsDisplay() } } }
        val tvRows = TextView(this).apply { id = 102; setTextColor(Color.WHITE); textSize = 14f; setPadding(8, 0, 8, 0); text = totalRows.toString() }
        val btnRowPlus = Button(this).apply { text = "+"; textSize = 14f; setPadding(0, 0, 0, 0); layoutParams = LinearLayout.LayoutParams(80, 80); setOnClickListener { totalRows++; updateRowsDisplay() } }
        rowsLayout.addView(btnRowMinus); rowsLayout.addView(tvRows); rowsLayout.addView(btnRowPlus)
        controlsLayout.addView(rowsLayout)
        fullHeaderLayout.addView(controlsLayout)

        val buttonsLayout = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            layoutParams = LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)
            gravity = Gravity.CENTER_VERTICAL
        }

        fun createSmallBtn(txt: String, onClick: () -> Unit): Button {
            return Button(this).apply {
                text = txt
                textSize = 10f
                setPadding(4, 0, 4, 0)
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
        fullHeaderLayout.addView(buttonsLayout)
        
        mainLayout.addView(fullHeaderLayout)"""

# Instead of using full match, let's just find the start and end indices using regex
start_match = re.search(r'\s*// Header\s*val headerLayout = LinearLayout\(this\)\.apply \{', content)
end_match = re.search(r'mainLayout\.addView\(headerLayout\)', content)

if start_match and end_match:
    start_idx = start_match.start()
    end_idx = end_match.end()
    content = content[:start_idx] + replacement + content[end_idx:]
    with open("app/src/main/java/com/example/SidebarEditActivity.kt", "w") as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Target not found via regex")

