import re

with open("app/src/main/java/com/example/service/PwaWindowManager.kt", "r") as f:
    content = f.read()

# Make default smaller
content = content.replace('prefs.getInt("pwa_${pwa.id}_width", 800)', 'prefs.getInt("pwa_${pwa.id}_width", 400)')
content = content.replace('prefs.getInt("pwa_${pwa.id}_height", 1000)', 'prefs.getInt("pwa_${pwa.id}_height", 500)')

search_col = """        Column(
            modifier = Modifier
                .fillMaxSize()
                .clip(if (isFullScreen) RoundedCornerShape(0.dp) else RoundedCornerShape(12.dp))
                .background(Color(0xFF1E1E2E))
        ) {"""
replace_col = """        Box(modifier = Modifier.fillMaxSize().clip(if (isFullScreen) RoundedCornerShape(0.dp) else RoundedCornerShape(12.dp)).background(Color(0xFF1E1E2E))) {
        Column(
            modifier = Modifier.fillMaxSize()
        ) {"""
content = content.replace(search_col, replace_col)

search_bottom = """                if (!isFullScreen) {
                    // Bottom controls
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(36.dp)
                    .background(Color(0xFF2A2A3C)),
                horizontalArrangement = Arrangement.End,
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = { 
                    onFold()
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
            }
        }
    }"""
replace_bottom = """                } // end column
                if (!isFullScreen) {
                    com.example.ui.WindowBottomControls(
                        onClose = onClose,
                        onMinimize = onFold,
                        onResize = onResize,
                        modifier = Modifier.align(Alignment.BottomEnd)
                    )
                }
            } // end outer box
        } // end Surface/Box? No, wait. Is there a Surface above it? No, in PwaWindowManager it is just Column initially.
    }"""
# Let's verify the exact structure in PwaWindowManager.kt
content = content.replace(search_bottom, replace_bottom)

with open("app/src/main/java/com/example/service/PwaWindowManager.kt", "w") as f:
    f.write(content)
