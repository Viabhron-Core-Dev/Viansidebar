import re

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "r") as f:
    content = f.read()

# Replace the specific handle_sidebar keys with a fallback checking startsWith
# Let's find the `when (key) {` block and add an else block or a condition in it.
# Actually, since it's `when (key) { ... }`, we can't do startsWith easily unless we change it.
# But wait, in Kotlin, `when` without an argument or `else -> if (key.startsWith("handle_")) ...`
# Let's see how the when block ends.
old_block = """            "handle_sidebar_y", "handle_sidebar_width", "handle_sidebar_height", "handle_sidebar_color", "handle_sidebar_shape" -> {
                triggerHandleView?.updatePosition()
            }"""

new_block = """            // We now handle dynamic keys at the end of the when block or using an else branch.
"""

content = content.replace(old_block, "")

# Same for reader handle?
# "handle_reader_y", "handle_reader_width", "handle_reader_height", "handle_reader_color", "handle_reader_shape" -> {
#                 readerHandleView?.updatePosition()
#             }

# Just replace `when (key) {` with `when (key) {` but add else branch
# Wait, let's just find `else -> {}` or end of `when(key)` and add it.
content = re.sub(
    r'}\s*val sidebarKeys',
    '} \n            else -> {\n                if (key != null && key.startsWith("handle_")) {\n                    triggerHandleViews.forEach { it.updatePosition() }\n                }\n            }\n        }\n        val sidebarKeys',
    content
)

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "w") as f:
    f.write(content)
