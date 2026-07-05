import re

with open('app/src/main/java/com/example/PageCustomizeScreen.kt', 'r') as f:
    content = f.read()

old_vars = """    var transparency by remember { mutableStateOf(page.transparency) }
    var title by remember { mutableStateOf(page.title) }"""
new_vars = """    var transparency by remember { mutableStateOf(page.transparency) }
    var title by remember { mutableStateOf(page.title) }
    var gridColumns by remember { mutableStateOf(page.gridColumns) }"""
content = content.replace(old_vars, new_vars)

old_save = """                val updatedPage = page.copy(
                    title = title,
                    useCustomSettings = useCustomSettings,
                    width = width,
                    height = height,
                    wrapContentHeight = wrapContentHeight,
                    transparency = transparency
                )"""
new_save = """                val updatedPage = page.copy(
                    title = title,
                    useCustomSettings = useCustomSettings,
                    width = width,
                    height = height,
                    wrapContentHeight = wrapContentHeight,
                    transparency = transparency,
                    gridColumns = gridColumns
                )"""
content = content.replace(old_save, new_save)

old_content = """                if (useCustomSettings) {
                    ListItem(
                        headlineContent = { Text("Width") },"""
new_content = """                if (useCustomSettings) {
                    if (page.type == "apps") {
                        ListItem(
                            headlineContent = { Text("App Grid Columns") },
                            supportingContent = {
                                Slider(
                                    value = gridColumns.toFloat(),
                                    onValueChange = { gridColumns = it.toInt() },
                                    valueRange = 2f..6f,
                                    steps = 3
                                )
                            },
                            trailingContent = { Text(gridColumns.toString()) }
                        )
                        Divider()
                    }
                    ListItem(
                        headlineContent = { Text("Width") },"""
content = content.replace(old_content, new_content)

with open('app/src/main/java/com/example/PageCustomizeScreen.kt', 'w') as f:
    f.write(content)
