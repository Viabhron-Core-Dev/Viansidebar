import re

with open("app/src/main/java/com/example/HandlesListSettingsScreen.kt", "r") as f:
    content = f.read()

# I will replace from `if (gesturesMap.isEmpty()) {` up to `Spacer(modifier = Modifier.height(16.dp))`
pattern = re.compile(r'if \(gesturesMap\.isEmpty\(\)\) \{.*?(?=Spacer\(modifier = Modifier\.height\(16\.dp\)\))', re.DOTALL)
new_code = """if (gesturesMap.isEmpty()) {
                        Text("No gestures assigned.", style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
                    } else {
                        gesturesMap.forEach { (gesture, action) ->
                            val actionName = when {
                                action == "toggle_sidebar" -> "Sidebar (Default)"
                                action == "toggle_reader" -> "Toggle Reader"
                                action.startsWith("open_page:") -> "Page: ${action.removePrefix("open_page:")}"
                                action.startsWith("action:") -> "Action: ${action.removePrefix("action:")}"
                                else -> action
                            }
                            
                            Card(
                                modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                                onClick = {
                                    if (action == "toggle_sidebar") {
                                        onNavigateToSidebarSettings()
                                    }
                                }
                            ) {
                                Row(
                                    modifier = Modifier.fillMaxWidth().padding(16.dp),
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.SpaceBetween
                                ) {
                                    Column(modifier = Modifier.weight(1f)) {
                                        Text(gestureLabels[gesture] ?: gesture, style = MaterialTheme.typography.titleSmall)
                                        Text(actionName, style = MaterialTheme.typography.bodyMedium)
                                    }
                                    var showGestureMenu by remember { mutableStateOf(false) }
                                    Box {
                                        IconButton(onClick = { showGestureMenu = true }) {
                                            Icon(Icons.Default.MoreVert, "More")
                                        }
                                        DropdownMenu(
                                            expanded = showGestureMenu,
                                            onDismissRequest = { showGestureMenu = false }
                                        ) {
                                            if (action == "toggle_sidebar") {
                                                DropdownMenuItem(
                                                    text = { Text("Sidebar Settings") },
                                                    onClick = {
                                                        showGestureMenu = false
                                                        onNavigateToSidebarSettings()
                                                    }
                                                )
                                            }
                                            DropdownMenuItem(
                                                text = { Text("Remove") },
                                                onClick = {
                                                    showGestureMenu = false
                                                    updateGesture(gesture, "none")
                                                }
                                            )
                                        }
                                    }
                                }
                            }
                        }
                    }
                    """

content = pattern.sub(new_code, content)

with open("app/src/main/java/com/example/HandlesListSettingsScreen.kt", "w") as f:
    f.write(content)
