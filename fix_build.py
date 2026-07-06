import re

with open('app/build.gradle.kts', 'r') as f:
    content = f.read()

content = content.replace('implementation("androidx.viewpager2:viewpager2:1.1.0")', 'implementation("androidx.viewpager2:viewpager2:1.1.0")\n    implementation("com.google.zxing:core:3.5.3")')

with open('app/build.gradle.kts', 'w') as f:
    f.write(content)
