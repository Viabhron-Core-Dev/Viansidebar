with open("app/src/main/java/com/example/service/ReaderHandleView.kt", "r") as f:
    content = f.read()

content = content.replace('openSidebarPage("apps")', 'openSidebarPage("sidebar", "apps")')

with open("app/src/main/java/com/example/service/ReaderHandleView.kt", "w") as f:
    f.write(content)
