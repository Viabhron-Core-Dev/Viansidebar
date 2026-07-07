import re

with open('app/src/main/java/com/example/service/CalculatorPageView.kt', 'r') as f:
    content = f.read()

old_eval = """fun evaluateExpression(expr: String): String {
    if (expr.isEmpty()) return ""
    try {
        val sanitized = expr.replace("x", "*").replace("÷", "/")
        val result = evalBasic(sanitized)
        if (result == result.toLong().toDouble()) {
            return result.toLong().toString()
        }
        return result.toString()
    } catch (e: Exception) {
        return "Error"
    }
}"""

new_eval = """fun evaluateExpression(expr: String): String {
    if (expr.isEmpty()) return ""
    try {
        val sanitized = expr.replace("x", "*").replace("÷", "/")
        val result = evalBasic(sanitized)
        if (result == result.toLong().toDouble()) {
            return result.toLong().toString()
        }
        return result.toString()
    } catch (e: Exception) {
        com.example.LogKeeper.writeLog("Calculator", "Evaluation error for expr $expr: ${e.message}")
        return "Error"
    }
}"""

content = content.replace(old_eval, new_eval)

with open('app/src/main/java/com/example/service/CalculatorPageView.kt', 'w') as f:
    f.write(content)

