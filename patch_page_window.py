import re

with open("app/src/main/java/com/example/service/PageWindowManager.kt", "r") as f:
    content = f.read()

# Make default smaller
content = content.replace('prefs.getInt("page_window_${pageType}_width", 800)', 'prefs.getInt("page_window_${pageType}_width", 400)')
content = content.replace('prefs.getInt("page_window_${pageType}_height", 1000)', 'prefs.getInt("page_window_${pageType}_height", 500)')

# Replace the layout
old_bottom = """            // Bottom controls
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(36.dp)
                    .background(Color(0xFF2A2A3C)),
                horizontalArrangement = Arrangement.End,
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = { 
                    onMinimize()
                }, modifier = Modifier.size(36.dp)) {
                    Icon(Icons.Default.KeyboardArrowDown, contentDescription = "Minimize", tint = Color.White, modifier = Modifier.size(20.dp))
                }
                IconButton(onClick = onClose, modifier = Modifier.size(36.dp)) {
                    Icon(Icons.Default.Close, contentDescription = "Close", tint = Color.White, modifier = Modifier.size(20.dp))
                }
                Box(
                    modifier = Modifier
                        .size(36.dp)
                        .background(Color(0xFF2A2A3C))
                        .pointerInput(Unit) {
                            detectDragGestures { change, dragAmount ->
                                change.consume()
                                onResize(dragAmount.x, dragAmount.y)
                            }
                        }
                ) {
                    Text("///", color = Color.Gray, modifier = Modifier.align(Alignment.Center).padding(end = 4.dp, bottom = 4.dp))
                }
            }
        }
    }"""

new_bottom = """        }

        // Overlay Bottom Controls
        Box(modifier = Modifier.fillMaxSize()) {
            com.example.ui.WindowBottomControls(
                onClose = onClose,
                onMinimize = onMinimize,
                onResize = onResize,
                modifier = Modifier.align(Alignment.BottomEnd)
            )
        }
    }
}"""
content = content.replace(old_bottom, new_bottom)

with open("app/src/main/java/com/example/service/PageWindowManager.kt", "w") as f:
    f.write(content)
