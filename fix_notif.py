import re

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'r') as f:
    content = f.read()

# Fix header click to also cancel
old_header_click = """                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable {
                                try {
                                    notification.contentIntent?.send()
                                } catch (e: Exception) {
                                    e.printStackTrace()
                                }
                            }
                            .padding(bottom = 4.dp)"""
new_header_click = """                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable {
                                try {
                                    notification.contentIntent?.send()
                                    AppNotificationListener.instance?.cancelNotification(sbn.key)
                                } catch (e: Exception) {
                                    e.printStackTrace()
                                }
                            }
                            .padding(bottom = 4.dp)"""
content = content.replace(old_header_click, new_header_click)

# Replace AlertDialog with a custom Box overlay
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
                .background(Color.Black.copy(alpha = 0.7f))
                .clickable { showFilterDialog = false },
            contentAlignment = Alignment.Center
        ) {
            Card(
                modifier = Modifier
                    .fillMaxWidth(0.9f)
                    .fillMaxHeight(0.8f)
                    .clickable { /* prevent dismiss */ },
                colors = CardDefaults.cardColors(containerColor = Color(0xFF1E1E1E))
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Filter Apps in Sidebar", style = MaterialTheme.typography.titleLarge, color = Color.White)
                    Spacer(modifier = Modifier.height(16.dp))
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
                                Text(name, color = Color.White)
                            }
                        }
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
                        TextButton(onClick = { showFilterDialog = false }) {
                            Text("Done", color = MaterialTheme.colorScheme.primary)
                        }
                    }
                }
            }
        }
    }"""
content = content.replace(old_dialog, new_dialog)

# The UI uses a Box, so the Box needs to fill the space
old_box = """                MaterialTheme(colorScheme = darkColorScheme()) {
                    Box(modifier = Modifier.onSizeChanged { size ->
                        if (currentHeightPx != size.height) {
                            currentHeightPx = size.height
                            onHeightChanged(size.height)
                        }
                    }) {
                        NotificationScreen(context)
                    }
                }"""
new_box = """                MaterialTheme(colorScheme = darkColorScheme()) {
                    Box(modifier = Modifier.fillMaxSize().onSizeChanged { size ->
                        if (currentHeightPx != size.height) {
                            currentHeightPx = size.height
                            onHeightChanged(size.height)
                        }
                    }) {
                        NotificationScreen(context)
                    }
                }"""
content = content.replace(old_box, new_box)

# Wrap Content Height for the main column -> fillMaxSize
old_col = "    Column(modifier = Modifier.fillMaxWidth().wrapContentHeight()) {"
new_col = "    Column(modifier = Modifier.fillMaxSize()) {"
content = content.replace(old_col, new_col)

# Make LazyColumn take remaining space
old_lazy = """        LazyColumn(
            modifier = Modifier
                .fillMaxWidth()
                .wrapContentHeight()
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {"""
new_lazy = """        LazyColumn(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {"""
content = content.replace(old_lazy, new_lazy)

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'w') as f:
    f.write(content)
