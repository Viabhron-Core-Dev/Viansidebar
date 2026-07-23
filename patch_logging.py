import re
import os

# AppTrackerPageView
with open("app/src/main/java/com/example/service/AppTrackerPageView.kt", "r") as f:
    content = f.read()

if "com.example.LogKeeper.writeLog(\"AppTracker\"" not in content:
    old_fun = "fun AppTrackerScreen(\n    context: Context,\n    onCloseSidebar: () -> Unit\n) {"
    new_fun = "fun AppTrackerScreen(\n    context: Context,\n    onCloseSidebar: () -> Unit\n) {\n    LaunchedEffect(Unit) {\n        com.example.LogKeeper.writeLog(\"AppTracker\", \"Opened app tracker page\")\n    }"
    content = content.replace(old_fun, new_fun)
    
    # Log actions
    content = content.replace("openAppInfo(context, it.packageName)", "com.example.LogKeeper.writeLog(\"AppTracker\", \"Opened app info for ${it.packageName}\"); openAppInfo(context, it.packageName)")

    with open("app/src/main/java/com/example/service/AppTrackerPageView.kt", "w") as f:
        f.write(content)

# DictionaryPageView
with open("app/src/main/java/com/example/service/DictionaryPageView.kt", "r") as f:
    content = f.read()

if "com.example.LogKeeper.writeLog(\"Dictionary\"" not in content:
    old_fun = "fun DictionaryScreen(context: Context, onCloseSidebar: (() -> Unit)?) {"
    new_fun = "fun DictionaryScreen(context: Context, onCloseSidebar: (() -> Unit)?) {\n    LaunchedEffect(Unit) {\n        com.example.LogKeeper.writeLog(\"Dictionary\", \"Opened dictionary page\")\n    }"
    content = content.replace(old_fun, new_fun)
    
    # Log search
    content = re.sub(r'onClick = \{\s*val q = searchQuery\.trim\(\)', 
                     "onClick = { val q = searchQuery.trim(); if(q.isNotEmpty()) { com.example.LogKeeper.writeLog(\"Dictionary\", \"Searched for: $q\") }", content)

    with open("app/src/main/java/com/example/service/DictionaryPageView.kt", "w") as f:
        f.write(content)

# PwaPageView
with open("app/src/main/java/com/example/service/PwaPageView.kt", "r") as f:
    content = f.read()

if "com.example.LogKeeper.writeLog(\"PWALoader\"" not in content:
    old_fun = "fun PwaScreen(context: Context, onCloseSidebar: (() -> Unit)?) {"
    new_fun = "fun PwaScreen(context: Context, onCloseSidebar: (() -> Unit)?) {\n    LaunchedEffect(Unit) {\n        com.example.LogKeeper.writeLog(\"PWALoader\", \"Opened PWA loader page\")\n    }"
    content = content.replace(old_fun, new_fun)

    # Log PWA launch
    content = content.replace("context.startActivity(i)", "com.example.LogKeeper.writeLog(\"PWALoader\", \"Launched PWA: ${pwa.name}\"); context.startActivity(i)")
    
    # Log Add New Pwa button
    content = content.replace("context.startActivity(Intent(context, PwaImportActivity::class.java))", "com.example.LogKeeper.writeLog(\"PWALoader\", \"Opened PWA Import Activity\"); context.startActivity(Intent(context, PwaImportActivity::class.java))")

    with open("app/src/main/java/com/example/service/PwaPageView.kt", "w") as f:
        f.write(content)

# WidgetsGridPageView
with open("app/src/main/java/com/example/service/WidgetsGridPageView.kt", "r") as f:
    content = f.read()
    
if "com.example.LogKeeper.writeLog(\"WidgetsGrid\"" not in content:
    old_init = "    init {\n        val scrollView = ScrollView(context).apply {"
    new_init = "    init {\n        com.example.LogKeeper.writeLog(\"WidgetsGrid\", \"Opened widgets grid page\")\n        val scrollView = ScrollView(context).apply {"
    content = content.replace(old_init, new_init)

    with open("app/src/main/java/com/example/service/WidgetsGridPageView.kt", "w") as f:
        f.write(content)

