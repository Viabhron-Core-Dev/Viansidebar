import re

def fix_gravity(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    # Find the init block where layoutParams is set.
    # gravity = Gravity.END or Gravity.TOP
    old_gravity = "gravity = Gravity.END or Gravity.TOP"
    new_gravity = """val isRight = prefs.getString("${prefix}edge", "right") == "right"
            gravity = (if (isRight) Gravity.END else Gravity.START) or Gravity.TOP"""

    content = content.replace(old_gravity, new_gravity)

    with open(file_path, "w") as f:
        f.write(content)

fix_gravity("app/src/main/java/com/example/service/TriggerHandleView.kt")
fix_gravity("app/src/main/java/com/example/service/ReaderHandleView.kt")
