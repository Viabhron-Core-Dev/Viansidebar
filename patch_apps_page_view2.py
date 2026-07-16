with open("app/src/main/java/com/example/service/AppsPageView.kt", "r") as f:
    content = f.read()

import re

target = re.compile(r"val pkg = item\.uri.*?getOrNull\(0\) \?: \"\"")

replacement = """val pkg = try {
                    android.content.Intent.parseUri(item.uri, android.content.Intent.URI_INTENT_SCHEME).`package` ?: android.content.Intent.parseUri(item.uri, android.content.Intent.URI_INTENT_SCHEME).component?.packageName ?: ""
                } catch (e: Exception) { "" }"""

content = target.sub(replacement, content)

with open("app/src/main/java/com/example/service/AppsPageView.kt", "w") as f:
    f.write(content)
