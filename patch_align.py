import re

with open("app/src/main/java/com/example/service/PwaWindowManager.kt", "r") as f:
    content = f.read()

search = """                } // end column
                if (!isFullScreen) {
                    com.example.ui.WindowBottomControls(
                        onClose = onClose,
                        onMinimize = onFold,
                        onResize = onResize,
                        modifier = Modifier.align(Alignment.BottomEnd)
                    )
                }
            } // end outer box"""
replace = """                } // end column
                if (!isFullScreen) {
                    Box(modifier = Modifier.fillMaxSize()) {
                        com.example.ui.WindowBottomControls(
                            onClose = onClose,
                            onMinimize = onFold,
                            onResize = onResize,
                            modifier = Modifier.align(Alignment.BottomEnd)
                        )
                    }
                }
            } // end outer box"""

content = content.replace(search, replace)

with open("app/src/main/java/com/example/service/PwaWindowManager.kt", "w") as f:
    f.write(content)
