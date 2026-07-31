import re

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # remaining windowContainer / tvContent usages in listener
    content = re.sub(r'                if \(::windowContainer\.isInitialized\) \{\n                    windowContainer\.keepScreenOn = sharedPreferences\.getBoolean\("keep_screen_on", true\)\n                \}\n', '', content)
    content = re.sub(r'                if \(::tvContent\.isInitialized\) \{\n                    tvContent\.textSize = 16f \* sharedPreferences\.getFloat\("font_size_scale", 1\.0f\)\n                \}\n', '', content)
    
    with open(path, 'w') as f:
        f.write(content)

fix_file('app/src/main/java/com/example/service/SidebarService.kt')
