with open("app/src/main/java/com/example/service/SidebarService.kt", "r") as f:
    content = f.read()

# I will find the else if (id.startsWith("page_window:")) and add else if (id.startsWith("floating_trigger:")) before it
pattern = '        } else if (id.startsWith("page_window:")) {'
replacement = """        } else if (id.startsWith("floating_trigger:")) {
            val targetId = id.removePrefix("floating_trigger:")
            val intent = Intent(this, com.example.service.FloatingTriggerService::class.java).apply {
                action = "TOGGLE"
                putExtra("TARGET_ID", targetId)
            }
            startService(intent)
        } else if (id.startsWith("page_window:")) {"""

content = content.replace(pattern, replacement)

with open("app/src/main/java/com/example/service/SidebarService.kt", "w") as f:
    f.write(content)

