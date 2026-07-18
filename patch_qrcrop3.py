import re

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "r") as f:
    content = f.read()

target = """            Button(onClick = {
                // Calculate scale
                val imgRatio = bitmap.width.toFloat() / bitmap.height.toFloat()
                val viewRatio = viewSize.width.toFloat() / viewSize.height.toFloat()
                
                var renderedW = viewSize.width.toFloat()
                var renderedH = viewSize.height.toFloat()
                var offsetX = 0f
                var offsetY = 0f
                
                if (imgRatio > viewRatio) {
                    renderedH = viewSize.width / imgRatio
                    offsetY = (viewSize.height - renderedH) / 2f
                } else {
                    renderedW = viewSize.height * imgRatio
                    offsetX = (viewSize.width - renderedW) / 2f
                }
                
                val scale = bitmap.width / renderedW
                
                val realX = (cropRect.left - offsetX) * scale
                val realY = (cropRect.top - offsetY) * scale
                val realW = cropRect.width * scale
                val realH = cropRect.height * scale
                
                onScan(realX, realY, realW, realH)
            }) {
                Text("Scan Selection")
            }"""

replacement = """            Button(onClick = {
                val imgRatio = bitmap.width.toFloat() / bitmap.height.toFloat()
                val viewRatio = viewSize.width.toFloat() / viewSize.height.toFloat()
                var renderedW = viewSize.width.toFloat()
                var renderedH = viewSize.height.toFloat()
                var offsetX = 0f
                var offsetY = 0f
                if (imgRatio > viewRatio) {
                    renderedH = viewSize.width / imgRatio
                    offsetY = (viewSize.height - renderedH) / 2f
                } else {
                    renderedW = viewSize.height * imgRatio
                    offsetX = (viewSize.width - renderedW) / 2f
                }
                val scale = bitmap.width / renderedW
                val realX = (cropRect.left - offsetX) * scale
                val realY = (cropRect.top - offsetY) * scale
                val realW = cropRect.width * scale
                val realH = cropRect.height * scale
                onAction("share", realX, realY, realW, realH)
            }) {
                Text("Share")
            }
            
            Button(onClick = {
                val imgRatio = bitmap.width.toFloat() / bitmap.height.toFloat()
                val viewRatio = viewSize.width.toFloat() / viewSize.height.toFloat()
                var renderedW = viewSize.width.toFloat()
                var renderedH = viewSize.height.toFloat()
                var offsetX = 0f
                var offsetY = 0f
                if (imgRatio > viewRatio) {
                    renderedH = viewSize.width / imgRatio
                    offsetY = (viewSize.height - renderedH) / 2f
                } else {
                    renderedW = viewSize.height * imgRatio
                    offsetX = (viewSize.width - renderedW) / 2f
                }
                val scale = bitmap.width / renderedW
                val realX = (cropRect.left - offsetX) * scale
                val realY = (cropRect.top - offsetY) * scale
                val realW = cropRect.width * scale
                val realH = cropRect.height * scale
                onAction("scan", realX, realY, realW, realH)
            }) {
                Text("Scan QR")
            }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "w") as f:
    f.write(content)
