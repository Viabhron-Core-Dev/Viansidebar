import os

files = [
    "app/src/main/java/com/example/service/PageWindowManager.kt",
    "app/src/main/java/com/example/service/WorkNotesWindowManager.kt",
    "app/src/main/java/com/example/service/DictionaryWindowManager.kt",
    "app/src/main/java/com/example/service/PwaWindowManager.kt"
]

target = """                }
            }"""
replacement = """                }
            }
        }"""

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        
        # We only want to replace the last occurrence that is related to the bottom controls, 
        # but let's just find the exact text of the bottom control box.
        
        target_full = """Text("///", color = Color.Gray, modifier = Modifier.align(Alignment.Center).padding(end = 4.dp, bottom = 4.dp))
                }
            }"""
        replacement_full = """Text("///", color = Color.Gray, modifier = Modifier.align(Alignment.Center).padding(end = 4.dp, bottom = 4.dp))
                }
            }
        }"""
        
        content = content.replace(target_full, replacement_full)
        
        with open(filepath, 'w') as f:
            f.write(content)

