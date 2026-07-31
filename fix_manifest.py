import re

with open('app/src/main/AndroidManifest.xml', 'r') as f:
    content = f.read()

content = content.replace('<service\n            android:name=".service.FloatingReaderService"\n            android:exported="false"\n            android:foregroundServiceType="mediaPlayback|microphone" />', 
                          '<service android:name=".service.SidebarService" android:exported="false" android:foregroundServiceType="mediaPlayback|microphone" />\n        <service android:name=".service.FloatingReaderService" android:exported="false" android:foregroundServiceType="mediaPlayback|microphone" />')

with open('app/src/main/AndroidManifest.xml', 'w') as f:
    f.write(content)
