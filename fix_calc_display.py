import re

with open('app/src/main/java/com/example/service/CalculatorPageView.kt', 'r') as f:
    content = f.read()

imports = [
    "import androidx.compose.foundation.horizontalScroll",
    "import androidx.compose.foundation.rememberScrollState",
    "import androidx.compose.runtime.LaunchedEffect"
]
for imp in imports:
    if imp not in content:
        content = content.replace('import androidx.compose.runtime.*', f'import androidx.compose.runtime.*\n{imp}')

start_marker = "// Display"
end_marker = "Spacer(modifier = Modifier.height(8.dp))"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx) + len(end_marker)

new_display = """// Display
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .weight(2f)
                .padding(vertical = 16.dp),
            verticalArrangement = Arrangement.Bottom,
            horizontalAlignment = Alignment.End
        ) {
            val scrollStateTop = rememberScrollState()
            val scrollStateBottom = rememberScrollState()
            
            LaunchedEffect(expression) {
                scrollStateTop.scrollTo(scrollStateTop.maxValue)
            }
            LaunchedEffect(resultText, expression) {
                scrollStateBottom.scrollTo(scrollStateBottom.maxValue)
            }

            val displayTextTop = if (resultText.isNotEmpty() || expressionCompleted) formatExpression(expression) else ""
            val displayTextBottom = when {
                expression.isEmpty() -> "0"
                resultText.isNotEmpty() -> resultText
                else -> formatExpression(expression)
            }

            if (displayTextTop.isNotEmpty()) {
                Row(
                    modifier = Modifier.fillMaxWidth().horizontalScroll(scrollStateTop),
                    horizontalArrangement = Arrangement.End
                ) {
                    Text(
                        text = displayTextTop,
                        fontSize = 28.sp,
                        color = Color.Gray,
                        textAlign = TextAlign.End,
                        maxLines = 1
                    )
                }
            } else {
                Spacer(modifier = Modifier.height(32.dp))
            }
            
            Spacer(modifier = Modifier.height(4.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth().horizontalScroll(scrollStateBottom),
                horizontalArrangement = Arrangement.End
            ) {
                Text(
                    text = displayTextBottom,
                    fontSize = 48.sp,
                    color = Color.White,
                    textAlign = TextAlign.End,
                    fontWeight = FontWeight.Medium,
                    maxLines = 1
                )
            }
        }
        
        Spacer(modifier = Modifier.height(8.dp))"""

content = content[:start_idx] + new_display + content[end_idx:]

with open('app/src/main/java/com/example/service/CalculatorPageView.kt', 'w') as f:
    f.write(content)

