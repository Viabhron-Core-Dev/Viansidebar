import re

with open("app/src/main/java/com/example/service/SchedulerPageView.kt", "r") as f:
    content = f.read()

content = content.replace("import com.example.AppDatabase\n", "import com.example.data.AppDatabase\n")
content = content.replace("import com.example.SchedulerTask\n", "import com.example.data.SchedulerTask\n")

with open("app/src/main/java/com/example/service/SchedulerPageView.kt", "w") as f:
    f.write(content)
