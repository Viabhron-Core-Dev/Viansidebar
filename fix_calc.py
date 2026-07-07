import re

with open('app/src/main/java/com/example/service/CalculatorPageView.kt', 'r') as f:
    content = f.read()

# Fix the evaluator issue where the last operator causes Error
# Also fix evalBasic issues if any (it throws RuntimeException on trailing operators, which we catch and return "Error")
# So if it returns "Error", resultText should be empty. Wait, the problem is evaluateExpression doesn't handle modulo % correctly sometimes, or maybe they just mean it returns Error.

# Update onInput
old_on_input = """        } else {
            expression += char
            val res = evaluateExpression(expression)
            if (res != "Error" && res.isNotEmpty() && expression.any { it in listOf('+', '-', 'x', '÷') }) {
                resultText = "=$res"
            } else {
                resultText = ""
            }
        }"""
new_on_input = """        } else {
            expression += char
            val res = evaluateExpression(expression)
            if (res != "Error" && res.isNotEmpty() && expression.any { it in listOf('+', '-', 'x', '÷', '%') }) {
                resultText = "=$res"
            } else {
                resultText = ""
            }
        }"""
content = content.replace(old_on_input, new_on_input)

old_on_delete = """        } else if (expression.isNotEmpty()) {
            expression = expression.dropLast(1)
            val res = evaluateExpression(expression)
            if (res != "Error" && res.isNotEmpty() && expression.any { it in listOf('+', '-', 'x', '÷') }) {
                resultText = "=$res"
            } else {
                resultText = ""
            }
        }"""
new_on_delete = """        } else if (expression.isNotEmpty()) {
            expression = expression.dropLast(1)
            val res = evaluateExpression(expression)
            if (res != "Error" && res.isNotEmpty() && expression.any { it in listOf('+', '-', 'x', '÷', '%') }) {
                resultText = "=$res"
            } else {
                resultText = ""
            }
        }"""
content = content.replace(old_on_delete, new_on_delete)

old_display = """        // Display
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .weight(2f)
                .padding(vertical = 16.dp),
            verticalArrangement = Arrangement.Bottom,
            horizontalAlignment = Alignment.End
        ) {
            Text(
                text = formatExpression(expression),
                fontSize = if (expressionCompleted) 32.sp else 48.sp,
                color = if (expressionCompleted) Color.Gray else Color.White,
                textAlign = TextAlign.End,
                lineHeight = 40.sp,
                maxLines = 3
            )
            if (resultText.isNotEmpty()) {
                Text(
                    text = resultText,
                    fontSize = if (expressionCompleted) 48.sp else 32.sp,
                    color = if (expressionCompleted) Color.White else Color.Gray,
                    textAlign = TextAlign.End,
                    fontWeight = FontWeight.Medium,
                    maxLines = 1
                )
            }
        }"""
new_display = """        // Display
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .weight(2f)
                .padding(vertical = 16.dp),
            verticalArrangement = Arrangement.Bottom,
            horizontalAlignment = Alignment.End
        ) {
            if (expression.isNotEmpty() && (resultText.isNotEmpty() || expressionCompleted)) {
                Text(
                    text = formatExpression(expression),
                    fontSize = 32.sp,
                    color = Color.Gray,
                    textAlign = TextAlign.End,
                    lineHeight = 40.sp,
                    maxLines = 3
                )
            } else if (expression.isNotEmpty()) {
                Text(
                    text = formatExpression(expression),
                    fontSize = 48.sp,
                    color = Color.White,
                    textAlign = TextAlign.End,
                    lineHeight = 40.sp,
                    maxLines = 3
                )
            }
            
            if (resultText.isNotEmpty()) {
                Text(
                    text = resultText,
                    fontSize = 48.sp,
                    color = Color.White,
                    textAlign = TextAlign.End,
                    fontWeight = FontWeight.Medium,
                    maxLines = 1
                )
            } else if (expression.isEmpty()) {
                Text(
                    text = "0",
                    fontSize = 48.sp,
                    color = Color.White,
                    textAlign = TextAlign.End,
                    fontWeight = FontWeight.Medium,
                    maxLines = 1
                )
            }
        }"""
content = content.replace(old_display, new_display)

with open('app/src/main/java/com/example/service/CalculatorPageView.kt', 'w') as f:
    f.write(content)
