import re

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "r") as f:
    content = f.read()

target = """    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {"""

replacement = """    override fun onBackPressed() {
        saveIds()
        super.onBackPressed()
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {"""

if "override fun onBackPressed()" not in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/SidebarEditActivity.kt", "w") as f:
        f.write(content)
    print("Patched back button")
else:
    print("Back button already patched")
