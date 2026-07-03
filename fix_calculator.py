import re

with open('app/src/main/java/com/example/service/CalculatorPageView.kt', 'r') as f:
    content = f.read()

# Replace .aspectRatio(1f) with .fillMaxHeight() inside the button Box modifier
content = content.replace('.aspectRatio(1f)', '.fillMaxHeight()')

with open('app/src/main/java/com/example/service/CalculatorPageView.kt', 'w') as f:
    f.write(content)

print("Fixed CalculatorPageView.")
