import re

with open('app/src/main/java/com/example/WelcomeScreen.kt', 'r') as f:
    content = f.read()

old_image = """        Icon(
            imageVector = androidx.compose.material.icons.Icons.Filled.Settings,
            contentDescription = "App Logo",
            modifier = Modifier.size(100.dp),
            tint = MaterialTheme.colorScheme.primary
        )"""

new_image = """        Icon(
            imageVector = androidx.compose.material.icons.Icons.Default.Check,
            contentDescription = "App Logo",
            modifier = Modifier.size(100.dp),
            tint = MaterialTheme.colorScheme.primary
        )"""

content = content.replace(old_image, new_image)

with open('app/src/main/java/com/example/WelcomeScreen.kt', 'w') as f:
    f.write(content)
