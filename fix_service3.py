import re

def remove_from_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # Remove createLongPressDragListener
    content = re.sub(r'    private fun createLongPressDragListener\(\): View\.OnTouchListener \{[\s\S]*?return false\n            \}\n        \}\n    \}\n', '', content)
    
    # Remove loadEpubCover
    content = re.sub(r'    private fun loadEpubCover\(file: java\.io\.File\): android\.graphics\.Bitmap\? \{[\s\S]*?return null\n    \}\n', '', content)
    
    # Remove getCoverCacheDir
    content = re.sub(r'    private fun getCoverCacheDir\(\): java\.io\.File \{[\s\S]*?return cacheDir\n    \}\n', '', content)
    
    with open(path, 'w') as f:
        f.write(content)

remove_from_file('app/src/main/java/com/example/service/SidebarService.kt')
