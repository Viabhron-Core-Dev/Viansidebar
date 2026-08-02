with open("app/src/main/java/com/example/AppTrackerSettingsActivity.kt", "r") as f:
    content = f.read()

content = content.replace("Image(bitmap = currentBitmap,", "val bmp = currentBitmap\n                            if (bmp != null) Image(bitmap = bmp,")

with open("app/src/main/java/com/example/AppTrackerSettingsActivity.kt", "w") as f:
    f.write(content)
