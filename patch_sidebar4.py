with open("app/src/main/java/com/example/service/SidebarService.kt", "r") as f:
    content = f.read()

content = content.replace("pageWindows[pageType]?.getCurrentHeightPx()", "pageWindows[pageType]?.height")
content = content.replace("pageWindows[pageType]?.height ?: 0", "pageWindows[pageType]?.layoutParams?.height ?: 0")

content = content.replace("removePwaWindow(id)", "removePwaWindow(id.toIntOrNull() ?: 0)")
content = content.replace("removePwaWindow(pwa.id.toString())", "removePwaWindow(pwa.id)")
content = content.replace("removePwaWindow(pageType)", "removePwaWindow(pageType.toIntOrNull() ?: 0)")

with open("app/src/main/java/com/example/service/SidebarService.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/service/SidebarView.kt", "r") as f:
    content2 = f.read()

content2 = content2.replace("mediaPlayerView?.getCurrentHeightPx()", "mediaPlayerView?.layoutParams?.height")

with open("app/src/main/java/com/example/service/SidebarView.kt", "w") as f:
    f.write(content2)

with open("app/src/main/java/com/example/AppTrackerSettingsActivity.kt", "r") as f:
    content3 = f.read()

content3 = content3.replace("val currentBitmap = bitmapState\n                        if (currentBitmap != null) {\n                            Image(bitmap = bitmapState,", "val currentBitmap = bitmapState\n                        if (currentBitmap != null) {\n                            Image(bitmap = currentBitmap,")

with open("app/src/main/java/com/example/AppTrackerSettingsActivity.kt", "w") as f:
    f.write(content3)
