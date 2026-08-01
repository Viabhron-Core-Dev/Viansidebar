import re

with open("app/src/main/java/com/example/service/DictionaryWindowManager.kt", "r") as f:
    content = f.read()

# Make default smaller
content = content.replace('prefs.getInt("dict_window_width", 600)', 'prefs.getInt("dict_window_width", 350)')
content = content.replace('prefs.getInt("dict_window_height", 800)', 'prefs.getInt("dict_window_height", 450)')
content = content.replace('.coerceAtLeast(400)', '.coerceAtLeast(300)')

search_surface = """        Surface(
            modifier = Modifier.fillMaxSize().clip(if (isFullScreen) RoundedCornerShape(0.dp) else RoundedCornerShape(12.dp)),
            color = Color(0xFF1E1E2C)
        ) {
            Column(modifier = Modifier.fillMaxSize()) {"""
replace_surface = """        Surface(
            modifier = Modifier.fillMaxSize().clip(if (isFullScreen) RoundedCornerShape(0.dp) else RoundedCornerShape(12.dp)),
            color = Color(0xFF1E1E2C)
        ) {
            Box(modifier = Modifier.fillMaxSize()) {
            Column(modifier = Modifier.fillMaxSize()) {"""
content = content.replace(search_surface, replace_surface)

search_bottom = """                // Bottom controls
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
replace_bottom = """            } // end column
            
            com.example.ui.WindowBottomControls(
                onClose = onClose,
                onMinimize = onFold,
                onResize = onResize,
                modifier = Modifier.align(Alignment.BottomEnd)
            )
            
            } // end Box
        } // end Surface
    }"""
content = content.replace(search_bottom, replace_bottom)

with open("app/src/main/java/com/example/service/DictionaryWindowManager.kt", "w") as f:
    f.write(content)
