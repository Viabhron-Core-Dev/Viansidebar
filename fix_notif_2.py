import re

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'r') as f:
    content = f.read()

# Add necessary imports
imports = [
    "import androidx.compose.material.icons.filled.ExpandMore",
    "import androidx.compose.material.icons.filled.ExpandLess",
    "import androidx.compose.material3.IconButton"
]
for imp in imports:
    if imp not in content:
        content = content.replace('import androidx.compose.material.icons.filled.FilterList', f'{imp}\nimport androidx.compose.material.icons.filled.FilterList')


# Modify filter dialog
old_filter_state = """    var hiddenPackages by remember { 
         mutableStateOf(prefs.getStringSet("hidden_packages", emptySet()) ?: emptySet())
    }"""
new_filter_state = """    var hiddenPackages by remember { 
         mutableStateOf(prefs.getStringSet("hidden_packages", emptySet()) ?: emptySet())
    }
    var historyHiddenPackages by remember {
         mutableStateOf(prefs.getStringSet("history_hidden_packages", prefs.getStringSet("hidden_packages", emptySet())) ?: emptySet())
    }"""
content = content.replace(old_filter_state, new_filter_state)

old_dialog_item = """                        items(appsInList) { (pkg, name) ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 4.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Checkbox(
                                    checked = !hiddenPackages.contains(pkg),
                                    onCheckedChange = { checked ->
                                        val newHidden = hiddenPackages.toMutableSet()
                                        if (checked) {
                                            newHidden.remove(pkg)
                                        } else {
                                            newHidden.add(pkg)
                                        }
                                        hiddenPackages = newHidden
                                        prefs.edit().putStringSet("hidden_packages", newHidden).apply()
                                    }
                                )
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(name, color = Color.White)
                            }
                        }"""
new_dialog_item = """                        items(appsInList) { (pkg, name) ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .combinedClickable(
                                        onClick = {
                                            val checked = hiddenPackages.contains(pkg)
                                            val newHidden = hiddenPackages.toMutableSet()
                                            if (checked) {
                                                newHidden.remove(pkg)
                                            } else {
                                                newHidden.add(pkg)
                                            }
                                            hiddenPackages = newHidden
                                            prefs.edit().putStringSet("hidden_packages", newHidden).apply()
                                        },
                                        onLongClick = {
                                            val newHistoryHidden = historyHiddenPackages.toMutableSet()
                                            if (newHistoryHidden.contains(pkg)) {
                                                newHistoryHidden.remove(pkg)
                                            } else {
                                                newHistoryHidden.add(pkg)
                                            }
                                            historyHiddenPackages = newHistoryHidden
                                            prefs.edit().putStringSet("history_hidden_packages", newHistoryHidden).apply()
                                        }
                                    )
                                    .padding(vertical = 4.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Checkbox(
                                    checked = !hiddenPackages.contains(pkg),
                                    onCheckedChange = { checked ->
                                        val newHidden = hiddenPackages.toMutableSet()
                                        if (checked) {
                                            newHidden.remove(pkg)
                                        } else {
                                            newHidden.add(pkg)
                                        }
                                        hiddenPackages = newHidden
                                        prefs.edit().putStringSet("hidden_packages", newHidden).apply()
                                    }
                                )
                                Spacer(modifier = Modifier.width(8.dp))
                                Column {
                                    Text(name, color = Color.White)
                                    if (historyHiddenPackages.contains(pkg)) {
                                        Text("History Disabled", color = Color.Gray, style = MaterialTheme.typography.bodySmall)
                                    }
                                }
                            }
                        }"""
content = content.replace(old_dialog_item, new_dialog_item)


# Modify NotificationItem
old_card_modifier = """                modifier = Modifier
                    .fillMaxWidth()
                    .combinedClickable(
                        onClick = {
                            expanded = !expanded
                        },
                        onLongClick = {
                            AppNotificationListener.instance?.cancelNotification(sbn.key)
                        }
                    ),"""
new_card_modifier = """                modifier = Modifier
                    .fillMaxWidth()
                    .combinedClickable(
                        onClick = {
                            try {
                                notification.contentIntent?.send()
                                AppNotificationListener.instance?.cancelNotification(sbn.key)
                            } catch (e: Exception) {
                                e.printStackTrace()
                            }
                        },
                        onLongClick = {
                            AppNotificationListener.instance?.cancelNotification(sbn.key)
                        }
                    ),"""
content = content.replace(old_card_modifier, new_card_modifier)

old_row = """                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable {
                                try {
                                    notification.contentIntent?.send()
                                    AppNotificationListener.instance?.cancelNotification(sbn.key)
                                } catch (e: Exception) {
                                    e.printStackTrace()
                                }
                            }
                            .padding(bottom = 4.dp)
                    ) {
                        Text(
                            text = appName,
                            style = MaterialTheme.typography.labelSmall,
                            color = Color.LightGray,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.weight(1f)
                        )
                    }"""
new_row = """                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(bottom = 4.dp)
                    ) {
                        Text(
                            text = appName,
                            style = MaterialTheme.typography.labelSmall,
                            color = Color.LightGray,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.weight(1f)
                        )
                        IconButton(
                            onClick = { expanded = !expanded },
                            modifier = Modifier.size(24.dp)
                        ) {
                            Icon(
                                imageVector = if (expanded) Icons.Default.ExpandLess else Icons.Default.ExpandMore,
                                contentDescription = if (expanded) "Collapse" else "Expand",
                                tint = Color.LightGray
                            )
                        }
                    }"""
content = content.replace(old_row, new_row)

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'w') as f:
    f.write(content)
