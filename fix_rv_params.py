import sys

with open('app/src/main/java/com/example/service/WidgetsGridEditOverlayView.kt', 'r') as f:
    content = f.read()

content = content.replace('ViewGroup.MarginLayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)', 
                          'RecyclerView.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)')

with open('app/src/main/java/com/example/service/WidgetsGridEditOverlayView.kt', 'w') as f:
    f.write(content)
