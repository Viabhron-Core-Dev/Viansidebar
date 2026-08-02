import re

# 1. HandleEditScreen: horizontal scroll for shapes
with open("app/src/main/java/com/example/HandleEditScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    'Text("Shape:")\n            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {',
    'Text("Shape:")\n            Row(modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(8.dp)) {'
)
with open("app/src/main/java/com/example/HandleEditScreen.kt", "w") as f:
    f.write(content)

# 2. SidebarService: readerHandleView?.updatePosition()
with open("app/src/main/java/com/example/service/SidebarService.kt", "r") as f:
    content = f.read()

content = content.replace(
    'if (key != null && key.startsWith("handle_") && key != "handles_list") {\n            triggerHandleViews.forEach { it.updatePosition() }\n        }',
    'if (key != null && key.startsWith("handle_") && key != "handles_list") {\n            triggerHandleViews.forEach { it.updatePosition() }\n            readerHandleView?.updatePosition()\n        }'
)
with open("app/src/main/java/com/example/service/SidebarService.kt", "w") as f:
    f.write(content)

# 3. FloatingReaderService: handle updates (if any handles exist)
with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "r") as f:
    content = f.read()

content = content.replace(
    'if (key != null && key.startsWith("handle_") && key != "handles_list") {\n            \n        }',
    'if (key != null && key.startsWith("handle_") && key != "handles_list") {\n            // The sidebar service manages readerHandleView updates now\n        }'
)
with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "w") as f:
    f.write(content)

# 4. SidebarSettingsScreen: remove columns slider
with open("app/src/main/java/com/example/SidebarSettingsScreen.kt", "r") as f:
    content = f.read()

content = re.sub(
    r'Divider\(\)\s*ListItem\(\s*headlineContent = \{ Text\("Columns \(Apps Grid\)"\) \}.*?trailingContent = \{ Text\(sidebarColumns\.toString\(\)\) \}\s*\)',
    '',
    content,
    flags=re.DOTALL
)
with open("app/src/main/java/com/example/SidebarSettingsScreen.kt", "w") as f:
    f.write(content)

