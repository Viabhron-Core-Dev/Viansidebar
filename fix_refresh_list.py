import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

content = content.replace('displayedItems = flatList\n        adapter.notifyDataSetChanged()', 'displayedItems = flatList\n        adapter.updateItems(flatList)')

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)

print("Fixed refreshList.")
