with open("app/src/main/java/com/example/service/QRCropActivity.kt", "r") as f:
    content = f.read()

content = content.replace("points.first().x - startX", "points.first().x - cropX")
content = content.replace("points.first().y - startY", "points.first().y - cropY")
content = content.replace("points[i].x - startX", "points[i].x - cropX")
content = content.replace("points[i].y - startY", "points[i].y - cropY")

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "w") as f:
    f.write(content)
