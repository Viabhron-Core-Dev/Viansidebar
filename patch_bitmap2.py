with open("app/src/main/java/com/example/AppTrackerSettingsActivity.kt", "r") as f:
    content = f.read()

content = content.replace("if (bitmapState != null) {\n                            Image(bitmap = bitmapState,", "val currentBitmap = bitmapState\n                        if (currentBitmap != null) {\n                            Image(bitmap = currentBitmap,")

with open("app/src/main/java/com/example/AppTrackerSettingsActivity.kt", "w") as f:
    f.write(content)
