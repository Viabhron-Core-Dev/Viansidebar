import re

with open("app/src/main/java/com/example/service/AppTrackerPageView.kt", "r") as f:
    content = f.read()

content = content.replace("import com.example.TrackedAppInfo\n", "")

tracked_app_class = """
data class TrackedAppInfo(
    val packageName: String,
    val appName: String,
    val lastUsedTime: Long = 0,
    val cacheSize: Long = 0
)

"""

if "data class TrackedAppInfo" not in content:
    with open("app/src/main/java/com/example/service/AppTrackerPageView.kt", "w") as f:
        f.write(content + "\n" + tracked_app_class)
