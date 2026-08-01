import os
import re

files = [
    "app/src/main/java/com/example/service/PageWindowManager.kt",
    "app/src/main/java/com/example/service/WorkNotesWindowManager.kt",
    "app/src/main/java/com/example/service/DictionaryWindowManager.kt",
    "app/src/main/java/com/example/service/PwaWindowManager.kt"
]

def fix_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r') as f:
        content = f.read()

    # Fix imports
    imports_to_add = """
import androidx.compose.foundation.gestures.detectDragGesturesAfterLongPress
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.material.icons.filled.KeyboardArrowDown
"""
    if "detectDragGesturesAfterLongPress" not in content[:content.find("class ")]:
        content = content.replace("import androidx.compose.foundation.gestures.detectDragGestures", imports_to_add)

    # Remove fully qualified name usage
    content = content.replace("androidx.compose.foundation.gestures.detectDragGesturesAfterLongPress", "detectDragGesturesAfterLongPress")
    content = content.replace("androidx.compose.foundation.gestures.detectDragGestures", "detectDragGestures")
    content = content.replace("androidx.compose.foundation.gestures.detectTapGestures", "detectTapGestures")

    # Fix the onFold / onMinimize compile error
    if "DictionaryWindowManager" in filepath:
        bad_str = """try { onMinimize() } catch(e: Exception) { 
                        try { onFold() } catch(e2: Exception) {}
                    }"""
        content = content.replace(bad_str, "onFold()")
    else:
        bad_str = """try { onMinimize() } catch(e: Exception) { 
                        try { onFold() } catch(e2: Exception) {}
                    }"""
        content = content.replace(bad_str, "onMinimize()")

    # For PwaWindowManager, remove duplicate isFullScreen variables and logic
    if "PwaWindowManager" in filepath:
        # PwaWindowManager has isFullScreen as a MutableState perhaps?
        pass # We will check this separately

    with open(filepath, 'w') as f:
        f.write(content)

for f in files:
    fix_file(f)

