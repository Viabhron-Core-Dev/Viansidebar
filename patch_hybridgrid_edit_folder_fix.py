import os
import re

with open("app/src/main/java/com/example/HybridGridEditActivity.kt", "r") as f:
    content = f.read()

# I will get the context at the beginning of the Composable
if 'val context = androidx.compose.ui.platform.LocalContext.current' not in content:
    content = content.replace('BoxWithConstraints(modifier = Modifier.fillMaxWidth().height(2000.dp)) {', 'val context = androidx.compose.ui.platform.LocalContext.current\n    BoxWithConstraints(modifier = Modifier.fillMaxWidth().height(2000.dp)) {')

# Fix onClick
content = content.replace('''val intent = android.content.Intent(androidx.compose.ui.platform.LocalContext.current, com.example.SidebarEditActivity::class.java).apply {''', '''val intent = android.content.Intent(context, com.example.SidebarEditActivity::class.java).apply {''')

content = content.replace('''val context = androidx.compose.ui.platform.LocalContext.current as? androidx.activity.ComponentActivity
                            context?.startActivityForResult(intent, 200)''', '''val activity = context as? androidx.activity.ComponentActivity
                            activity?.startActivityForResult(intent, 200)''')

# Fix Icons.Default.Edit
content = content.replace('''androidx.compose.material.icons.Icons.Default.Edit''', '''androidx.compose.material.icons.filled.Edit''')

with open("app/src/main/java/com/example/HybridGridEditActivity.kt", "w") as f:
    f.write(content)
