import re

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "r") as f:
    content = f.read()

# Check if already has receiver
if "private val iconUpdateReceiver" not in content:
    receiver_code = """
    private val iconUpdateReceiver = object : android.content.BroadcastReceiver() {
        override fun onReceive(context: Context, intent: Intent) {
            val itemId = intent.getStringExtra("item_id")
            if (itemId != null) {
                appsManager.iconCache.remove("custom_$itemId")
                appsManager.iconCache.remove(itemId)
                // Reload widgets to refresh the UI
                loadWidgets()
            }
        }
    }

    override fun onAttachedToWindow() {
        super.onAttachedToWindow()
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
            context.registerReceiver(iconUpdateReceiver, android.content.IntentFilter("com.example.UPDATE_SIDEBAR_ICONS"), Context.RECEIVER_NOT_EXPORTED)
        } else {
            context.registerReceiver(iconUpdateReceiver, android.content.IntentFilter("com.example.UPDATE_SIDEBAR_ICONS"))
        }
    }

    override fun onDetachedFromWindow() {
        super.onDetachedFromWindow()
        try {
            context.unregisterReceiver(iconUpdateReceiver)
        } catch(e: Exception) {}
    }
}"""
    # Replace last brace
    content = content.rstrip()
    if content.endswith("}"):
        content = content[:-1] + receiver_code
    
    with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "w") as f:
        f.write(content)
