#!/bin/bash
awk '
/fun getIconBitmap/ {
    print "    fun getIconBitmap(id: String): Bitmap? {"
    print "        val customIconFile = java.io.File(context.filesDir, \"custom_icons/${id.replace(Regex(\"[^a-zA-Z0-9.-]\"), \"_\")}.webp\")"
    print "        if (customIconFile.exists()) {"
    print "            var b = iconCache.get(\"custom_$id\")"
    print "            if (b == null) {"
    print "                try {"
    print "                    b = android.graphics.BitmapFactory.decodeFile(customIconFile.absolutePath)"
    print "                    if (b != null) iconCache.put(\"custom_$id\", b)"
    print "                } catch(e: Exception) {}"
    print "            }"
    print "            if (b != null) return b"
    print "        }"
    in_func = 1
    next
}
in_func == 1 && /if \(id.startsWith\("app:"\)\)/ {
    in_func = 0
    print
    next
}
{ print }
' app/src/main/java/com/example/service/SidebarAppsManager.kt > temp.kt && mv temp.kt app/src/main/java/com/example/service/SidebarAppsManager.kt
