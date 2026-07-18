import re

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "r") as f:
    content = f.read()

target = """        if (viewSize.width > 0) {
            Canvas(modifier = Modifier
                .fillMaxSize()
                .pointerInput(Unit) {
                    detectDragGestures { change, dragAmount ->
                        change.consume()
                        cropRect = cropRect.translate(dragAmount.x, dragAmount.y)
                    }
                }
            ) {
                // Dim background
                drawRect(Color.Black.copy(alpha = 0.5f))
                
                // Cutout center
                drawRect(
                    color = Color.Transparent,
                    topLeft = cropRect.topLeft,
                    size = cropRect.size,
                    blendMode = androidx.compose.ui.graphics.BlendMode.Clear
                )
                
                // Draw border
                drawRect(
                    color = Color.Green,
                    topLeft = cropRect.topLeft,
                    size = cropRect.size,
                    style = Stroke(width = 4.dp.toPx())
                )
            }
        }"""

replacement = """        if (viewSize.width > 0) {
            val handleSize = 40.dp
            
            Canvas(modifier = Modifier
                .fillMaxSize()
                .pointerInput(Unit) {
                    var dragHandle: String? = null
                    detectDragGestures(
                        onDragStart = { offset ->
                            val touchRadius = 60.dp.toPx()
                            val left = cropRect.left
                            val right = cropRect.right
                            val top = cropRect.top
                            val bottom = cropRect.bottom
                            
                            dragHandle = when {
                                offset.x in (left - touchRadius)..(left + touchRadius) && offset.y in (top - touchRadius)..(top + touchRadius) -> "topLeft"
                                offset.x in (right - touchRadius)..(right + touchRadius) && offset.y in (top - touchRadius)..(top + touchRadius) -> "topRight"
                                offset.x in (left - touchRadius)..(left + touchRadius) && offset.y in (bottom - touchRadius)..(bottom + touchRadius) -> "bottomLeft"
                                offset.x in (right - touchRadius)..(right + touchRadius) && offset.y in (bottom - touchRadius)..(bottom + touchRadius) -> "bottomRight"
                                offset.x in left..right && offset.y in top..bottom -> "center"
                                else -> null
                            }
                        },
                        onDragEnd = { dragHandle = null },
                        onDragCancel = { dragHandle = null },
                        onDrag = { change, dragAmount ->
                            change.consume()
                            when (dragHandle) {
                                "topLeft" -> cropRect = Rect(cropRect.left + dragAmount.x, cropRect.top + dragAmount.y, cropRect.right, cropRect.bottom)
                                "topRight" -> cropRect = Rect(cropRect.left, cropRect.top + dragAmount.y, cropRect.right + dragAmount.x, cropRect.bottom)
                                "bottomLeft" -> cropRect = Rect(cropRect.left + dragAmount.x, cropRect.top, cropRect.right, cropRect.bottom + dragAmount.y)
                                "bottomRight" -> cropRect = Rect(cropRect.left, cropRect.top, cropRect.right + dragAmount.x, cropRect.bottom + dragAmount.y)
                                "center" -> cropRect = cropRect.translate(dragAmount.x, dragAmount.y)
                            }
                            
                            // Enforce minimum size and constraints
                            if (cropRect.width < 50f) cropRect = Rect(cropRect.left, cropRect.top, cropRect.left + 50f, cropRect.bottom)
                            if (cropRect.height < 50f) cropRect = Rect(cropRect.left, cropRect.top, cropRect.right, cropRect.top + 50f)
                        }
                    )
                }
            ) {
                // Dim background
                drawRect(Color.Black.copy(alpha = 0.5f))
                
                // Cutout center
                drawRect(
                    color = Color.Transparent,
                    topLeft = cropRect.topLeft,
                    size = cropRect.size,
                    blendMode = androidx.compose.ui.graphics.BlendMode.Clear
                )
                
                // Draw border
                drawRect(
                    color = Color.Green,
                    topLeft = cropRect.topLeft,
                    size = cropRect.size,
                    style = Stroke(width = 4.dp.toPx())
                )
                
                // Draw handles
                val hs = handleSize.toPx() / 2
                drawCircle(Color.Green, radius = hs, center = cropRect.topLeft)
                drawCircle(Color.Green, radius = hs, center = cropRect.topRight)
                drawCircle(Color.Green, radius = hs, center = cropRect.bottomLeft)
                drawCircle(Color.Green, radius = hs, center = cropRect.bottomRight)
            }
        }"""
content = content.replace(target, replacement)

target2 = """            Button(onClick = {
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
                
                onAction("scan", realX, realY, realW, realH)
            }) {
                Text("Scan Selection")
            }"""

replacement2 = """            Button(onClick = {
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
content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "w") as f:
    f.write(content)
