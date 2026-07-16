with open("app/src/main/java/com/example/AppPickerActivity.kt", "r") as f:
    content = f.read()

import re
content = re.sub(
    r'scope\.launch \{\s*val loaded = manager\.loadIcon\(appInfo\.packageName\)\s*withContext\(Dispatchers\.Main\) \{\s*if \(loaded != null\) \{\s*view\.findViewById<ImageView>\(1\)\.setImageBitmap\(loaded\)\s*\}\s*\}\s*\}',
    """val imgView = view.findViewById<ImageView>(1)
                            imgView.tag = appInfo.packageName
                            scope.launch {
                                val loaded = manager.loadIcon(appInfo.packageName)
                                withContext(Dispatchers.Main) {
                                    if (loaded != null && imgView.tag == appInfo.packageName) {
                                        imgView.setImageBitmap(loaded)
                                    }
                                }
                            }""",
    content
)

with open("app/src/main/java/com/example/AppPickerActivity.kt", "w") as f:
    f.write(content)
