with open("app/src/main/java/com/example/AppTrackerSettingsActivity.kt", "r") as f:
    content = f.read()

content = content.replace("true\n            else if (searchQuery.isNotBlank())", "if (searchQuery.isNotBlank())")

with open("app/src/main/java/com/example/AppTrackerSettingsActivity.kt", "w") as f:
    f.write(content)
