import os
import re

with open("app/src/main/java/com/example/HybridGridEditActivity.kt", "r") as f:
    content = f.read()

content = content.replace(
'''                            )
                        }
                ) {
                    Icon(painter = androidx.compose.ui.res.painterResource(android.R.drawable.ic_menu_crop), contentDescription = "Resize", tint = Color.White)
                }''',
'''                            )
                        }
                    ) {
                        Icon(painter = androidx.compose.ui.res.painterResource(android.R.drawable.ic_menu_crop), contentDescription = "Resize", tint = Color.White)
                    }
                }''')

with open("app/src/main/java/com/example/HybridGridEditActivity.kt", "w") as f:
    f.write(content)
