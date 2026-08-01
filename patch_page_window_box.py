import re

with open("app/src/main/java/com/example/service/PageWindowManager.kt", "r") as f:
    content = f.read()

# I will replace the PageWindowContent structure.
# From Column(...) { to the end of the new_bottom.

search_content = """        Column(
            modifier = Modifier
                .fillMaxSize()
                .clip(RoundedCornerShape(12.dp))
                .background(Color(0xFF1E1E2E))
        ) {"""

replace_content = """        Box(modifier = Modifier.fillMaxSize().clip(RoundedCornerShape(12.dp)).background(Color(0xFF1E1E2E))) {
        Column(
            modifier = Modifier.fillMaxSize()
        ) {"""
content = content.replace(search_content, replace_content)

# Now fix the end

search_end = """        }

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
replace_end = """        } // end column

        // Overlay Bottom Controls
        com.example.ui.WindowBottomControls(
            onClose = onClose,
            onMinimize = onMinimize,
            onResize = onResize,
            modifier = Modifier.align(Alignment.BottomEnd)
        )
    } // end outer box
    }
}"""
content = content.replace(search_end, replace_end)

with open("app/src/main/java/com/example/service/PageWindowManager.kt", "w") as f:
    f.write(content)
