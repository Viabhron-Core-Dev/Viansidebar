import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

content = content.replace('if (currentSpan == 3) {', 'if (currentSpan == (if (pageConfig?.useCustomSettings == true) pageConfig.gridColumns else prefs.getInt("sidebar_columns", 4))) {')

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)

