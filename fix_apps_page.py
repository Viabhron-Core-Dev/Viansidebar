import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

content = content.replace("override fun onReceive(context: Context, intent: Intent)", "override fun onReceive(context: Context, intent: android.content.Intent)")
content = content.replace("android.content.IntentFilter", "android.content.IntentFilter") # redundant
# Wait, "Unresolved reference 'getStringExtra'" means intent is still treated as un-imported if not fully qualified!
# So replacing with android.content.Intent works.

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)
