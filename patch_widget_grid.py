import sys

with open('app/src/main/java/com/example/service/WidgetsGridPageView.kt', 'r') as f:
    content = f.read()

target = """                        val hostView = host.createView(context, widgetId, info)
                        addView(hostView, LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT))"""

replacement = """                        val hostView = host.createView(context, widgetId, info)
                        val params = LinearLayout.LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT).apply {
                            gravity = Gravity.CENTER_HORIZONTAL
                        }
                        addView(hostView, params)"""

content = content.replace(target, replacement)

with open('app/src/main/java/com/example/service/WidgetsGridPageView.kt', 'w') as f:
    f.write(content)
