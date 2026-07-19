import re

with open('app/src/main/java/com/example/service/AppNotificationListener.kt', 'r') as f:
    content = f.read()

pattern = """        // Record history
        if \\(sbn\\.isClearable\\) \\{
            val prefs = getSharedPreferences\\("NotificationPrefs", Context\\.MODE_PRIVATE\\)"""

replacement = """        // Record history
        if (true) { // removed isClearable check to save all notifications
            val prefs = getSharedPreferences("NotificationPrefs", Context.MODE_PRIVATE)"""

content = re.sub(pattern, replacement, content)

# Let's also extract EXTRA_BIG_TEXT, EXTRA_SUB_TEXT, and tickerText
pattern_text = """                        val text = notification\\.extras\\.getCharSequence\\(android\\.app\\.Notification\\.EXTRA_TEXT\\)\\?\\.toString\\(\\) \\?: \"\""""

replacement_text = """                        val text = notification.extras.getCharSequence(android.app.Notification.EXTRA_TEXT)?.toString() 
                            ?: notification.extras.getCharSequence(android.app.Notification.EXTRA_BIG_TEXT)?.toString()
                            ?: notification.extras.getCharSequence(android.app.Notification.EXTRA_SUB_TEXT)?.toString()
                            ?: notification.tickerText?.toString()
                            ?: "" """

content = re.sub(pattern_text, replacement_text, content)

with open('app/src/main/java/com/example/service/AppNotificationListener.kt', 'w') as f:
    f.write(content)
