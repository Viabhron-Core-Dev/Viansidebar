import re

with open('app/src/main/java/com/example/SettingsActivity.kt', 'r') as f:
    content = f.read()

old_screen = re.search(r'@OptIn\(ExperimentalMaterial3Api::class\)\n@Composable\nfun ScreenCapSettingsScreen.*?\}\n\}\n', content, re.DOTALL).group(0)

new_screen = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ScreenCapSettingsScreen(onBack: () -> Unit) {
    val context = LocalContext.current
    val prefs = remember { context.getSharedPreferences("ScreenCapPrefs", Context.MODE_PRIVATE) }
    
    var saveLocation by remember { mutableStateOf(prefs.getString("save_location", "Default (Pictures/Screenshots)") ?: "Default (Pictures/Screenshots)") }
    var delaySeconds by remember { mutableStateOf(prefs.getInt("screenshot_delay", 0)) }

    val dirLauncher = androidx.activity.compose.rememberLauncherForActivityResult(
        contract = androidx.activity.result.contract.ActivityResultContracts.OpenDocumentTree()
    ) { uri ->
        if (uri != null) {
            context.contentResolver.takePersistableUriPermission(
                uri,
                Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION
            )
            val path = uri.toString()
            prefs.edit().putString("save_location", path).apply()
            saveLocation = path
            Toast.makeText(context, "Location saved", Toast.LENGTH_SHORT).show()
        }
    }

    Column(modifier = Modifier.fillMaxSize()) {
        TopAppBar(
            title = { Text("Screen Cap Settings") },
            navigationIcon = {
                IconButton(onClick = onBack) {
                    Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                }
            }
        )
        LazyColumn(modifier = Modifier.fillMaxSize().padding(16.dp)) {
            item {
                Text(
                    text = "Save Location",
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.padding(bottom = 8.dp)
                )
                Text(
                    text = saveLocation,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(bottom = 16.dp)
                )
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { dirLauncher.launch(null) }) {
                        Text("Change Location")
                    }
                    Button(onClick = { 
                        prefs.edit().putString("save_location", "Default (Pictures/Screenshots)").apply()
                        saveLocation = "Default (Pictures/Screenshots)"
                    }, colors = ButtonDefaults.outlinedButtonColors()) {
                        Text("Reset")
                    }
                }
                
                Divider(modifier = Modifier.padding(vertical = 24.dp))
                
                Text(
                    text = "Screenshot Delay",
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.padding(bottom = 8.dp)
                )
                Text(
                    text = "Delay before capturing screen: ${delaySeconds}s",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(bottom = 8.dp)
                )
                Slider(
                    value = delaySeconds.toFloat(),
                    onValueChange = { 
                        delaySeconds = it.toInt()
                        prefs.edit().putInt("screenshot_delay", delaySeconds).apply()
                    },
                    valueRange = 0f..10f,
                    steps = 9
                )
            }
        }
    }
}
"""

content = content.replace(old_screen, new_screen)

with open('app/src/main/java/com/example/SettingsActivity.kt', 'w') as f:
    f.write(content)
