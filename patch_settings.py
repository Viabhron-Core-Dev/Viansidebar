import re

with open("app/src/main/java/com/example/AppTrackerSettingsActivity.kt", "r") as f:
    content = f.read()

# Add auto_force_stop state
pattern_state = r'var showSystemApps by remember \{ mutableStateOf\(prefs\.getBoolean\("app_tracker_show_system", false\)\) \}'
repl_state = r'''var showSystemApps by remember { mutableStateOf(prefs.getBoolean("app_tracker_show_system", false)) }
    var autoForceStop by remember { mutableStateOf(prefs.getBoolean("app_tracker_auto_force_stop", false)) }'''
content = re.sub(pattern_state, repl_state, content)

# Add auto_force_stop switch to UI before the Search Apps field
pattern_ui = r'OutlinedTextField\(\s*value = searchQuery,'
repl_ui = r'''Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text("Auto Force Stop (Accessibility)")
                Switch(
                    checked = autoForceStop,
                    onCheckedChange = { 
                        autoForceStop = it
                        prefs.edit().putBoolean("app_tracker_auto_force_stop", it).apply()
                    }
                )
            }
            
            OutlinedTextField(
                value = searchQuery,'''
content = re.sub(pattern_ui, repl_ui, content)

with open("app/src/main/java/com/example/AppTrackerSettingsActivity.kt", "w") as f:
    f.write(content)
