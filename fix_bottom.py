import os
import re

files = [
    "app/src/main/java/com/example/service/PageWindowManager.kt",
    "app/src/main/java/com/example/service/WorkNotesWindowManager.kt",
    "app/src/main/java/com/example/service/DictionaryWindowManager.kt",
    "app/src/main/java/com/example/service/PwaWindowManager.kt"
]

def process_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r') as f:
        content = f.read()

    # We want to replace everything from '// Resize handle' up to the matching closing brace of the Box.
    # A simple way is to use regex with DOTALL, finding '// Resize handle' and up to 'Text("///"' and its enclosing Box.
    
    # Let's do a more manual string search and replace
    start_idx = content.find('// Resize handle')
    if start_idx != -1:
        # find the end of the Box which should be 'Text("///"' ... ) \n            }
        end_str = 'Text("///"'
        text_idx = content.find(end_str, start_idx)
        if text_idx != -1:
            end_bracket_idx = content.find('}', text_idx)
            if end_bracket_idx != -1:
                end_bracket_idx = content.find('}', end_bracket_idx + 1)
                if end_bracket_idx != -1:
                    replacement = """// Bottom controls
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(36.dp)
                    .background(Color(0xFF2A2A3C)),
                horizontalArrangement = Arrangement.End,
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = { 
                    try { onMinimize() } catch(e: Exception) { 
                        try { onFold() } catch(e2: Exception) {}
                    }
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
                            androidx.compose.foundation.gestures.detectDragGestures { change, dragAmount ->
                                change.consume()
                                onResize(dragAmount.x, dragAmount.y)
                            }
                        }
                ) {
                    Text("///", color = Color.Gray, modifier = Modifier.align(Alignment.Center).padding(end = 4.dp, bottom = 4.dp))
                }
            }"""
                    content = content[:start_idx] + replacement + content[end_bracket_idx+1:]
    
    with open(filepath, 'w') as f:
        f.write(content)

for f in files:
    process_file(f)

