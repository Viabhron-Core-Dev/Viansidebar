import re

with open("app/src/main/java/com/example/service/DictionaryPageView.kt", "r") as f:
    content = f.read()

replacement = """
        Row(
            modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text("Dictionary", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.White)
            Row {
                IconButton(onClick = { 
                    (context as? FloatingReaderService)?.toggleDictionaryWindow() 
                }, modifier = Modifier.size(28.dp)) {
                    Icon(androidx.compose.material.icons.Icons.Default.OpenInNew, contentDescription = "Pop out", tint = Color.LightGray)
                }
                Spacer(modifier = Modifier.width(8.dp))
                IconButton(onClick = onCloseSidebar, modifier = Modifier.size(28.dp)) {
                    Icon(Icons.Default.Close, contentDescription = "Close", tint = Color.LightGray)
                }
            }
        }
"""

content = re.sub(
    r'Row\(\s*modifier = Modifier.fillMaxWidth\(\).padding\(bottom = 8.dp\),\s*verticalAlignment = Alignment.CenterVertically,\s*horizontalArrangement = Arrangement.SpaceBetween\s*\)\s*\{[\s\S]*?IconButton\(onClick = onCloseSidebar, modifier = Modifier.size\(28.dp\)\) \{\s*Icon\(Icons.Default.Close, contentDescription = "Close", tint = Color.LightGray\)\s*\}\s*\}',
    replacement.strip(),
    content
)

content = "import androidx.compose.material.icons.filled.OpenInNew\n" + content

with open("app/src/main/java/com/example/service/DictionaryPageView.kt", "w") as f:
    f.write(content)
