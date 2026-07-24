import os
import re

with open("app/src/main/java/com/example/HybridGridEditActivity.kt", "r") as f:
    content = f.read()

content = content.replace('BoxWithConstraints(modifier = Modifier.fillMaxWidth().height(2000.dp)) {', 'val context = androidx.compose.ui.platform.LocalContext.current\n    BoxWithConstraints(modifier = Modifier.fillMaxWidth().height(2000.dp)) {')

content = content.replace('androidx.compose.material.icons.filled.Edit', 'androidx.compose.material.icons.Icons.Filled.Edit')

with open("app/src/main/java/com/example/HybridGridEditActivity.kt", "w") as f:
    f.write(content)
