with open("app/src/main/java/com/example/service/AppsPageView.kt", "r") as f:
    content = f.read()

target = """                } else if (item is SidebarItem.SystemAction) {"""

replacement = """                } else if (item is SidebarItem.IntentAction) {
                    try {
                        val intent = android.content.Intent.parseUri(item.uri, android.content.Intent.URI_INTENT_SCHEME)
                        intent.addFlags(android.content.Intent.FLAG_ACTIVITY_NEW_TASK)
                        context.startActivity(intent)
                    } catch (e: Exception) {
                        e.printStackTrace()
                    }
                    currentFolderPopup?.dismiss()
                    onCloseSidebar()
                } else if (item is SidebarItem.SystemAction) {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/AppsPageView.kt", "w") as f:
    f.write(content)
