import re

with open('app/src/main/java/com/example/service/CalculatorPageView.kt', 'r') as f:
    content = f.read()

# Make the Display weight 2f
content = content.replace('.weight(1f)\n                .padding(vertical = 16.dp)', '.weight(2f)\n                .padding(vertical = 16.dp)')

# Make each Row weight 1f
content = content.replace('.fillMaxWidth().padding(vertical = 6.dp)', '.fillMaxWidth().weight(1f).padding(vertical = 4.dp)')

with open('app/src/main/java/com/example/service/CalculatorPageView.kt', 'w') as f:
    f.write(content)

print("Fixed CalculatorPageView rows.")
