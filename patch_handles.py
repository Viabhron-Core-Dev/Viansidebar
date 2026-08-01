with open("app/src/main/java/com/example/HandlesListSettingsScreen.kt", "r") as f:
    content = f.read()

import re

# Add state for gesture to change
search_state = "var showAddGestureDialog by remember { mutableStateOf(false) }"
replace_state = """var showAddGestureDialog by remember { mutableStateOf(false) }
                    var showChangeGestureDialog by remember { mutableStateOf(false) }
                    var gestureToChange by remember { mutableStateOf("") }"""
content = content.replace(search_state, replace_state)

# Add DropdownMenuItem for Change
search_menu = """                                            if (action == "toggle_sidebar") {
                                                DropdownMenuItem(
                                                    text = { Text("Sidebar Settings") },
                                                    onClick = {
                                                        showGestureMenu = false
                                                        onNavigateToSidebarSettings(gesture, null)
                                                    }
                                                )
                                            }
                                            DropdownMenuItem(
                                                text = { Text("Remove") },"""
replace_menu = """                                            if (action == "toggle_sidebar") {
                                                DropdownMenuItem(
                                                    text = { Text("Sidebar Settings") },
                                                    onClick = {
                                                        showGestureMenu = false
                                                        onNavigateToSidebarSettings(gesture, null)
                                                    }
                                                )
                                            }
                                            DropdownMenuItem(
                                                text = { Text("Change") },
                                                onClick = {
                                                    showGestureMenu = false
                                                    gestureToChange = gesture
                                                    showChangeGestureDialog = true
                                                }
                                            )
                                            DropdownMenuItem(
                                                text = { Text("Remove") },"""
content = content.replace(search_menu, replace_menu)

# Copy the showAddGestureDialog block and change it to showChangeGestureDialog
# We'll do it manually using regex since the block is long.
# Actually I can just write it.

change_dialog = """                    if (showChangeGestureDialog) {
                        val context = LocalContext.current
                        val pageConfigs = com.example.utils.PageManager.getPages(prefs, handle.id)
                        
                        val categoryOptions = listOf(
                            "page" to "Page",
                            "element" to "Action/Element",
                            "sidebar" to "Sidebar"
                        )
                        var selectedCategory by remember { mutableStateOf(categoryOptions.first().first) }
                        var selectedPageType by remember { mutableStateOf(if (pageConfigs.isNotEmpty()) pageConfigs.first().type else "") }
                        
                        AlertDialog(
                            onDismissRequest = { showChangeGestureDialog = false },
                            title = { Text("Change Action for ${gestureLabels[gestureToChange] ?: gestureToChange}") },
                            text = {
                                Column {
                                    ActionDropdown("Type/Content", selectedCategory, categoryOptions) { selectedCategory = it }
                                    
                                    if (selectedCategory == "page") {
                                        Spacer(modifier = Modifier.height(8.dp))
                                        val pageOptions = listOf(
                                            "apps" to "Apps Grid",
                                            "widgets_grid" to "Widgets Grid",
                                            "hybrid_grid" to "Hybrid Grid",
                                            "app_tracker" to "App Tracker",
                                            "calculator" to "Calculator",
                                            "scheduler" to "Scheduler",
                                            "compass" to "Compass",
                                            "notifications" to "Notifications"
                                        )
                                        if (selectedPageType.isEmpty()) selectedPageType = "apps"
                                        ActionDropdown("Select Page", selectedPageType, pageOptions) { selectedPageType = it }
                                    }
                                }
                            },
                            confirmButton = {
                                TextButton(onClick = {
                                    if (selectedCategory == "sidebar") {
                                        updateGesture(gestureToChange, "toggle_sidebar")
                                        showChangeGestureDialog = false
                                    } else if (selectedCategory == "page") {
                                        if (selectedPageType.isNotEmpty()) {
                                            updateGesture(gestureToChange, "open_page:$selectedPageType")
                                            showChangeGestureDialog = false
                                        }
                                    } else if (selectedCategory == "element") {
                                        val intent = android.content.Intent(context, com.example.AddElementActivity::class.java).apply {
                                            action = "SELECT_ELEMENT_FOR_HANDLE"
                                            putExtra("handle_prefix", prefix)
                                            putExtra("gesture", gestureToChange)
                                            addFlags(android.content.Intent.FLAG_ACTIVITY_NEW_TASK)
                                        }
                                        context.startActivity(intent)
                                        showChangeGestureDialog = false
                                    }
                                }) {
                                    Text("Change")
                                }
                            },
                            dismissButton = {
                                TextButton(onClick = { showChangeGestureDialog = false }) {
                                    Text("Cancel")
                                }
                            }
                        )
                    }"""

search_add_dialog_start = "                    if (showAddGestureDialog) {"
replace_add_dialog = change_dialog + "\n\n" + search_add_dialog_start
content = content.replace(search_add_dialog_start, replace_add_dialog)

# Also need to add "sidebar" to categoryOptions in add dialog, because it's missing but it was handled.
search_add_categories = """                        val categoryOptions = listOf(
                            "page" to "Page",
                            "element" to "Action/Element"
                        )"""
replace_add_categories = """                        val categoryOptions = listOf(
                            "page" to "Page",
                            "element" to "Action/Element",
                            "sidebar" to "Sidebar"
                        )"""
content = content.replace(search_add_categories, replace_add_categories)

with open("app/src/main/java/com/example/HandlesListSettingsScreen.kt", "w") as f:
    f.write(content)

