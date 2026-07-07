import re

with open('app/src/main/java/com/example/service/CalculatorPageView.kt', 'r') as f:
    content = f.read()

# Remove % from parseTerm
old_parseTerm = """        fun parseTerm(): Double {
            var x = parseFactor()
            while (true) {
                if (eat('*'.toInt())) x *= parseFactor() // multiplication
                else if (eat('/'.toInt())) x /= parseFactor() // division
                else if (eat('%'.toInt())) x %= parseFactor() // modulo
                else return x
            }
        }"""
new_parseTerm = """        fun parseTerm(): Double {
            var x = parseFactor()
            while (true) {
                if (eat('*'.toInt())) x *= parseFactor() // multiplication
                else if (eat('/'.toInt())) x /= parseFactor() // division
                else return x
            }
        }"""
content = content.replace(old_parseTerm, new_parseTerm)

# Add % to parseFactor as a postfix operator
old_parseFactor = """            if (eat('('.toInt())) { // parentheses
                x = parseExpression()
                eat(')'.toInt())
            } else if (ch >= '0'.toInt() && ch <= '9'.toInt() || ch == '.'.toInt()) { // numbers
                while (ch >= '0'.toInt() && ch <= '9'.toInt() || ch == '.'.toInt()) nextChar()
                x = str.substring(startPos, pos).toDouble()
            } else {
                throw RuntimeException("Unexpected: " + ch.toChar())
            }
            return x"""
new_parseFactor = """            if (eat('('.toInt())) { // parentheses
                x = parseExpression()
                eat(')'.toInt())
            } else if (ch >= '0'.toInt() && ch <= '9'.toInt() || ch == '.'.toInt()) { // numbers
                while (ch >= '0'.toInt() && ch <= '9'.toInt() || ch == '.'.toInt()) nextChar()
                x = str.substring(startPos, pos).toDouble()
            } else {
                throw RuntimeException("Unexpected: " + ch.toChar())
            }
            while (eat('%'.toInt())) {
                x /= 100.0
            }
            return x"""
content = content.replace(old_parseFactor, new_parseFactor)

with open('app/src/main/java/com/example/service/CalculatorPageView.kt', 'w') as f:
    f.write(content)
