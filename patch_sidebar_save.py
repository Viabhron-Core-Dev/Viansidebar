import re

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "r") as f:
    content = f.read()

target = """    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 100 && resultCode == RESULT_OK) {
            val id = data?.getStringExtra("ELEMENT_ID")
            if (id != null) {
                localIds.add(id)
                adapter.notifyItemInserted(localIds.size - 1)
            }
        } else if (requestCode == 200 && resultCode == RESULT_OK) {
            val updatedFolder = data?.getStringExtra("UPDATED_FOLDER")
            val uuid = data?.getStringExtra("FOLDER_UUID")
            if (updatedFolder != null && uuid != null) {
                val index = localIds.indexOfFirst { it.startsWith("folder:$uuid:") }
                if (index != -1) {
                    localIds[index] = updatedFolder
                    adapter.notifyItemChanged(index)
                }
            }
        }
    }"""

replacement = """    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 100 && resultCode == RESULT_OK) {
            val id = data?.getStringExtra("ELEMENT_ID")
            if (id != null) {
                localIds.add(id)
                adapter.notifyItemInserted(localIds.size - 1)
                saveIds() // Auto-save after addition
            }
        } else if (requestCode == 200 && resultCode == RESULT_OK) {
            val updatedFolder = data?.getStringExtra("UPDATED_FOLDER")
            val uuid = data?.getStringExtra("FOLDER_UUID")
            if (updatedFolder != null && uuid != null) {
                val index = localIds.indexOfFirst { it.startsWith("folder:$uuid:") }
                if (index != -1) {
                    localIds[index] = updatedFolder
                    adapter.notifyItemChanged(index)
                    saveIds() // Auto-save after folder edit
                }
            }
        }
    }"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "w") as f:
    f.write(content)
