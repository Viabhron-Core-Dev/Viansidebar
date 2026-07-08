import re

with open('app/src/main/java/com/example/NotificationHistoryActivity.kt', 'r') as f:
    content = f.read()

old_dialog = """        if (showFilterDialog) {
            AlertDialog(
                onDismissRequest = { showFilterDialog = false },
                title = { Text("Filter Apps in History") },
                text = {
                    val pm = context.packageManager
                    // Get a list of all packages we have in history to filter
                    val appsInHistory = history.map { it.packageName to it.appName }.distinctBy { it.first }
                    
                    LazyColumn {
                        items(appsInHistory) { (pkg, name) ->
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
                                        prefs.edit().putStringSet("history_hidden_packages", newHidden).apply()
                                    }
                                )
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(name)
                            }
                        }
                    }
                },
                confirmButton = {
                    TextButton(onClick = { showFilterDialog = false }) {
                        Text("Done")
                    }
                }
            )
        }"""

new_dialog = """        if (showFilterDialog) {
            androidx.compose.ui.window.Dialog(onDismissRequest = { showFilterDialog = false }) {
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .fillMaxHeight(0.8f)
                        .padding(16.dp),
                    shape = androidx.compose.foundation.shape.RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
                ) {
                    Column(modifier = Modifier.padding(24.dp).fillMaxSize()) {
                        Text(
                            text = "Filter Apps in History",
                            style = MaterialTheme.typography.titleLarge,
                            modifier = Modifier.padding(bottom = 16.dp)
                        )
                        
                        val pm = context.packageManager
                        val appsInHistory = history.map { it.packageName to it.appName }.distinctBy { it.first }
                        
                        LazyColumn(modifier = Modifier.weight(1f)) {
                            items(appsInHistory) { (pkg, name) ->
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
                                            prefs.edit().putStringSet("history_hidden_packages", newHidden).apply()
                                        }
                                    )
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text(name)
                                }
                            }
                        }
                        
                        Row(
                            modifier = Modifier.fillMaxWidth().padding(top = 16.dp),
                            horizontalArrangement = Arrangement.End
                        ) {
                            TextButton(onClick = { showFilterDialog = false }) {
                                Text("Done")
                            }
                        }
                    }
                }
            }
        }"""

if old_dialog in content:
    content = content.replace(old_dialog, new_dialog)
    with open('app/src/main/java/com/example/NotificationHistoryActivity.kt', 'w') as f:
        f.write(content)
    print("Replaced in NotificationHistoryActivity.kt")
else:
    print("Failed to find old dialog in NotificationHistoryActivity.kt")

