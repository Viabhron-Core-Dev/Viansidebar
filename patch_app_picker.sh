#!/bin/bash
sed -i 's/        manager = SidebarAppsManager(this, getSharedPreferences("prefs", Context.MODE_PRIVATE), CoroutineScope(Dispatchers.IO)) {/        manager = SidebarAppsManager(this, getSharedPreferences("prefs", Context.MODE_PRIVATE), CoroutineScope(Dispatchers.IO)) {/' app/src/main/java/com/example/AppPickerActivity.kt

awk '
{
    print $0
    if ($0 ~ /setContentView\(layout\)/) {
        found = 1
    }
}
'
