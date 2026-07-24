import os
import re

with open("app/src/main/java/com/example/HybridGridEditActivity.kt", "r") as f:
    content = f.read()

# Add an edit button for folders
pattern = r'if \(item\.id\.startsWith\("widget:"\)\) \{'

repl = '''if (item.id.startsWith("folder:")) {
                    IconButton(
                        onClick = {
                            val uuid = item.id.split(":")[1]
                            val intent = android.content.Intent(androidx.compose.ui.platform.LocalContext.current, com.example.SidebarEditActivity::class.java).apply {
                                putExtra("FOLDER_UUID", uuid)
                                putExtra("FOLDER_FULL_ID", item.id)
                            }
                            val context = androidx.compose.ui.platform.LocalContext.current as? androidx.activity.ComponentActivity
                            context?.startActivityForResult(intent, 200)
                        },
                        modifier = Modifier.align(Alignment.BottomStart).size(24.dp).padding(4.dp).background(Color.Blue, shape = androidx.compose.foundation.shape.CircleShape)
                    ) {
                        Icon(androidx.compose.material.icons.Icons.Default.Edit, contentDescription = "Edit", tint = Color.White, modifier = Modifier.size(16.dp))
                    }
                }
                
                if (item.id.startsWith("widget:")) {'''

content = content.replace('if (item.id.startsWith("widget:")) {', repl, 1)

with open("app/src/main/java/com/example/HybridGridEditActivity.kt", "w") as f:
    f.write(content)
