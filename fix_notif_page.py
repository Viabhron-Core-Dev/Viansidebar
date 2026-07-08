import re

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'r') as f:
    content = f.read()

old_dialog = """    if (showFilterDialog) {
        AlertDialog(
            onDismissRequest = { showFilterDialog = false },
            title = { Text("Filter Apps in Sidebar") },
            text = {
                val pm = context.packageManager
                // Get all apps that ever posted a notification in our current active list
                val appsInList = notifications.map { it.packageName to 
                    try { pm.getApplicationLabel(pm.getApplicationInfo(it.packageName, 0)).toString() } 
                    catch(e: Exception) { it.packageName }
                }.distinctBy { it.first }
                
                LazyColumn {
                    items(appsInList) { (pkg, name) ->
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

new_dialog = """    if (showFilterDialog) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color.Black.copy(alpha = 0.6f))
                .clickable(
                    interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                    indication = null
                ) { showFilterDialog = false },
            contentAlignment = Alignment.Center
        ) {
            Card(
                modifier = Modifier
                    .fillMaxWidth(0.9f)
                    .fillMaxHeight(0.8f)
                    .padding(16.dp),
                shape = androidx.compose.foundation.shape.RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
            ) {
                Column(modifier = Modifier.padding(24.dp).fillMaxSize()) {
                    Text(
                        text = "Filter Apps in Sidebar",
                        style = MaterialTheme.typography.titleLarge,
                        modifier = Modifier.padding(bottom = 16.dp)
                    )
                    
                    val pm = context.packageManager
                    val appsInList = notifications.map { it.packageName to 
                        try { pm.getApplicationLabel(pm.getApplicationInfo(it.packageName, 0)).toString() } 
                        catch(e: Exception) { it.packageName }
                    }.distinctBy { it.first }
                    
                    LazyColumn(modifier = Modifier.weight(1f)) {
                        items(appsInList) { (pkg, name) ->
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
    with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'w') as f:
        f.write(content)
    print("Replaced in NotificationPageView.kt")
else:
    print("Failed to find old dialog in NotificationPageView.kt")

