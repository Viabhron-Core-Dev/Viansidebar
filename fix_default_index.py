with open("app/src/main/java/com/example/utils/PageManager.kt", "r") as f:
    content = f.read()

content = content.replace(
    'fun getDefaultPageIndex(prefs: SharedPreferences): Int {\n        return prefs.getInt("sidebar_default_page_index", 0)\n    }',
    'fun getDefaultPageIndex(prefs: SharedPreferences, handleId: String): Int {\n        return prefs.getInt("handle_${handleId}_default_page_index", prefs.getInt("sidebar_default_page_index", 0))\n    }'
)

content = content.replace(
    'fun saveDefaultPageIndex(prefs: SharedPreferences, index: Int) {\n        prefs.edit().putInt("sidebar_default_page_index", index).apply()\n    }',
    'fun saveDefaultPageIndex(prefs: SharedPreferences, handleId: String, index: Int) {\n        prefs.edit().putInt("handle_${handleId}_default_page_index", index).apply()\n    }'
)

with open("app/src/main/java/com/example/utils/PageManager.kt", "w") as f:
    f.write(content)
