with open("app/src/main/java/com/example/service/AppNotificationListener.kt", "r") as f:
    content = f.read()
content = content.replace(
    'val historyHidden = prefs.getStringSet("history_hidden_packages", prefs.getStringSet("hidden_packages", emptySet())) ?: emptySet()',
    'val historyHidden = prefs.getStringSet("history_hidden_packages", emptySet()) ?: emptySet()'
)
with open("app/src/main/java/com/example/service/AppNotificationListener.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/NotificationHistoryActivity.kt", "r") as f:
    content = f.read()
content = content.replace(
    'mutableStateOf(prefs.getStringSet("history_hidden_packages", prefs.getStringSet("hidden_packages", emptySet())) ?: emptySet())',
    'mutableStateOf(prefs.getStringSet("history_hidden_packages", emptySet()) ?: emptySet())'
)
with open("app/src/main/java/com/example/NotificationHistoryActivity.kt", "w") as f:
    f.write(content)
