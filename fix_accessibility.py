with open('app/src/main/res/xml/accessibility_service_config.xml', 'r') as f:
    content = f.read()

content = content.replace('<accessibility-service xmlns:android="http://schemas.android.com/apk/res/android"', '<accessibility-service xmlns:android="http://schemas.android.com/apk/res/android"\n    android:canTakeScreenshot="true"')

with open('app/src/main/res/xml/accessibility_service_config.xml', 'w') as f:
    f.write(content)
