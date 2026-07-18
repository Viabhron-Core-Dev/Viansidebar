import re

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "r") as f:
    content = f.read()

# 1. Update onAction signature in QRCropScreen
content = content.replace(
    "fun QRCropScreen(bitmap: Bitmap, onAction: (String, Float, Float, Float, Float, String) -> Unit, onClose: () -> Unit) {",
    "fun QRCropScreen(bitmap: Bitmap, onAction: (String, Float, Float, Float, Float, String, List<Offset>) -> Unit, onClose: () -> Unit) {"
)

# Add polygonPoints state
content = content.replace(
    "var cropShape by remember { mutableStateOf(\"square\") }",
    "var cropShape by remember { mutableStateOf(\"square\") }\n    val polygonPoints = remember { mutableStateListOf<Offset>() }"
)

# 2. Update pointerInput
target_pointerInput = """                .pointerInput(Unit) {
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
                }"""

replacement_pointerInput = """                .pointerInput(cropShape) {
                    if (cropShape == "polygon") {
                        androidx.compose.foundation.gestures.detectTapGestures { offset ->
                            polygonPoints.add(offset)
                        }
                    } else {
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
                }"""
content = content.replace(target_pointerInput, replacement_pointerInput)

# 3. Update drawing path
target_path = """                val path = androidx.compose.ui.graphics.Path().apply {
                    addRect(androidx.compose.ui.geometry.Rect(0f, 0f, size.width, size.height))
                    if (cropShape == "circle") {
                        addOval(cropRect)
                    } else if (cropShape == "polygon") {
                        // Draw a hexagon
                        val cx = cropRect.center.x
                        val cy = cropRect.center.y
                        val rx = cropRect.width / 2f
                        val ry = cropRect.height / 2f
                        moveTo(cx, cy - ry)
                        lineTo(cx + rx * 0.866f, cy - ry * 0.5f)
                        lineTo(cx + rx * 0.866f, cy + ry * 0.5f)
                        lineTo(cx, cy + ry)
                        lineTo(cx - rx * 0.866f, cy + ry * 0.5f)
                        lineTo(cx - rx * 0.866f, cy - ry * 0.5f)
                        close()
                    } else {
                        addRect(cropRect)
                    }
                    fillType = androidx.compose.ui.graphics.PathFillType.EvenOdd
                }
                drawPath(path, dimColor)
                
                if (cropShape == "circle") {
                    drawOval(Color.Green, cropRect.topLeft, cropRect.size, style = Stroke(width = 4.dp.toPx()))
                } else if (cropShape == "polygon") {
                    val hexPath = androidx.compose.ui.graphics.Path().apply {
                        val cx = cropRect.center.x
                        val cy = cropRect.center.y
                        val rx = cropRect.width / 2f
                        val ry = cropRect.height / 2f
                        moveTo(cx, cy - ry)
                        lineTo(cx + rx * 0.866f, cy - ry * 0.5f)
                        lineTo(cx + rx * 0.866f, cy + ry * 0.5f)
                        lineTo(cx, cy + ry)
                        lineTo(cx - rx * 0.866f, cy + ry * 0.5f)
                        lineTo(cx - rx * 0.866f, cy - ry * 0.5f)
                        close()
                    }
                    drawPath(hexPath, Color.Green, style = Stroke(width = 4.dp.toPx()))
                } else {
                    drawRect(Color.Green, cropRect.topLeft, cropRect.size, style = Stroke(width = 4.dp.toPx()))
                }
                
                // Draw handles
                val hs = handleSize.toPx() / 2
                drawCircle(Color.Green, radius = hs, center = cropRect.topLeft)
                drawCircle(Color.Green, radius = hs, center = cropRect.topRight)
                drawCircle(Color.Green, radius = hs, center = cropRect.bottomLeft)
                drawCircle(Color.Green, radius = hs, center = cropRect.bottomRight)"""

replacement_path = """                val path = androidx.compose.ui.graphics.Path().apply {
                    addRect(androidx.compose.ui.geometry.Rect(0f, 0f, size.width, size.height))
                    if (cropShape == "circle") {
                        addOval(cropRect)
                    } else if (cropShape == "polygon") {
                        if (polygonPoints.isNotEmpty()) {
                            moveTo(polygonPoints.first().x, polygonPoints.first().y)
                            for (i in 1 until polygonPoints.size) {
                                lineTo(polygonPoints[i].x, polygonPoints[i].y)
                            }
                            close()
                        }
                    } else {
                        addRect(cropRect)
                    }
                    fillType = androidx.compose.ui.graphics.PathFillType.EvenOdd
                }
                drawPath(path, dimColor)
                
                val hs = handleSize.toPx() / 2
                if (cropShape == "circle") {
                    drawOval(Color.Green, cropRect.topLeft, cropRect.size, style = Stroke(width = 4.dp.toPx()))
                } else if (cropShape == "polygon") {
                    if (polygonPoints.isNotEmpty()) {
                        val polyPath = androidx.compose.ui.graphics.Path().apply {
                            moveTo(polygonPoints.first().x, polygonPoints.first().y)
                            for (i in 1 until polygonPoints.size) {
                                lineTo(polygonPoints[i].x, polygonPoints[i].y)
                            }
                            close()
                        }
                        drawPath(polyPath, Color.Green, style = Stroke(width = 4.dp.toPx()))
                        polygonPoints.forEach { pt ->
                            drawCircle(Color.Green, radius = hs, center = pt)
                        }
                    }
                } else {
                    drawRect(Color.Green, cropRect.topLeft, cropRect.size, style = Stroke(width = 4.dp.toPx()))
                }
                
                // Draw handles for square and circle
                if (cropShape != "polygon") {
                    drawCircle(Color.Green, radius = hs, center = cropRect.topLeft)
                    drawCircle(Color.Green, radius = hs, center = cropRect.topRight)
                    drawCircle(Color.Green, radius = hs, center = cropRect.bottomLeft)
                    drawCircle(Color.Green, radius = hs, center = cropRect.bottomRight)
                }"""
content = content.replace(target_path, replacement_path)

# 4. Update the Hex button to Polygon
content = content.replace(
    'Text("Hex", modifier = Modifier.padding(8.dp))',
    'Text("Polygon", modifier = Modifier.padding(8.dp))'
)
# Add a clear button for polygon
target_buttons = """        Column(
            modifier = Modifier
                .align(Alignment.CenterEnd)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            FloatingActionButton(onClick = { cropShape = "square" }, containerColor = if (cropShape == "square") Color.Green else Color.Gray) {
                Text("Square", modifier = Modifier.padding(8.dp))
            }
            FloatingActionButton(onClick = { cropShape = "circle" }, containerColor = if (cropShape == "circle") Color.Green else Color.Gray) {
                Text("Circle", modifier = Modifier.padding(8.dp))
            }
            FloatingActionButton(onClick = { cropShape = "polygon" }, containerColor = if (cropShape == "polygon") Color.Green else Color.Gray) {
                Text("Polygon", modifier = Modifier.padding(8.dp))
            }
        }"""

replacement_buttons = """        Column(
            modifier = Modifier
                .align(Alignment.CenterEnd)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            FloatingActionButton(onClick = { cropShape = "square" }, containerColor = if (cropShape == "square") Color.Green else Color.Gray) {
                Text("Square", modifier = Modifier.padding(8.dp))
            }
            FloatingActionButton(onClick = { cropShape = "circle" }, containerColor = if (cropShape == "circle") Color.Green else Color.Gray) {
                Text("Circle", modifier = Modifier.padding(8.dp))
            }
            FloatingActionButton(onClick = { cropShape = "polygon" }, containerColor = if (cropShape == "polygon") Color.Green else Color.Gray) {
                Text("Polygon", modifier = Modifier.padding(8.dp))
            }
            if (cropShape == "polygon" && polygonPoints.isNotEmpty()) {
                FloatingActionButton(onClick = { polygonPoints.clear() }, containerColor = Color.Red) {
                    Text("Clear", modifier = Modifier.padding(8.dp), color = Color.White)
                }
            }
        }"""
content = content.replace(target_buttons, replacement_buttons)

# 5. Update onAction call inside QRCropScreen
target_onAction = """            Button(onClick = {
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
                onAction("share", realX, realY, realW, realH, cropShape)
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
                onAction("scan", realX, realY, realW, realH, cropShape)
            }) {
                Text("Scan QR")
            }"""

replacement_onAction = """            Button(onClick = {
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
                val minX = polygonPoints.minOfOrNull { it.x } ?: 0f
                val maxX = polygonPoints.maxOfOrNull { it.x } ?: 0f
                val minY = polygonPoints.minOfOrNull { it.y } ?: 0f
                val maxY = polygonPoints.maxOfOrNull { it.y } ?: 0f
                val rectToUse = if (cropShape == "polygon" && polygonPoints.isNotEmpty()) Rect(minX, minY, maxX, maxY) else cropRect
                
                val realX = (rectToUse.left - offsetX) * scale
                val realY = (rectToUse.top - offsetY) * scale
                val realW = rectToUse.width * scale
                val realH = rectToUse.height * scale
                val mappedPoints = polygonPoints.map { Offset((it.x - offsetX) * scale, (it.y - offsetY) * scale) }
                onAction("share", realX, realY, realW, realH, cropShape, mappedPoints)
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
                val minX = polygonPoints.minOfOrNull { it.x } ?: 0f
                val maxX = polygonPoints.maxOfOrNull { it.x } ?: 0f
                val minY = polygonPoints.minOfOrNull { it.y } ?: 0f
                val maxY = polygonPoints.maxOfOrNull { it.y } ?: 0f
                val rectToUse = if (cropShape == "polygon" && polygonPoints.isNotEmpty()) Rect(minX, minY, maxX, maxY) else cropRect
                
                val realX = (rectToUse.left - offsetX) * scale
                val realY = (rectToUse.top - offsetY) * scale
                val realW = rectToUse.width * scale
                val realH = rectToUse.height * scale
                val mappedPoints = polygonPoints.map { Offset((it.x - offsetX) * scale, (it.y - offsetY) * scale) }
                onAction("scan", realX, realY, realW, realH, cropShape, mappedPoints)
            }) {
                Text("Scan QR")
            }"""
content = content.replace(target_onAction, replacement_onAction)

# 6. Update Activity onCreate call to QRCropScreen
content = content.replace(
    "                QRCropScreen(",
    "                QRCropScreen("
)
target_onCreate_action = """                    onAction = { action, x, y, w, h, shape ->
                        if (action == "share") {
                            shareCroppedArea(bitmap, x, y, w, h, shape)
                        } else if (action == "scan") {
                            scanCroppedArea(bitmap, x, y, w, h, shape)
                        }
                    },"""
replacement_onCreate_action = """                    onAction = { action, x, y, w, h, shape, points ->
                        if (action == "share") {
                            shareCroppedArea(bitmap, x, y, w, h, shape, points)
                        } else if (action == "scan") {
                            scanCroppedArea(bitmap, x, y, w, h, shape, points)
                        }
                    },"""
content = content.replace(target_onCreate_action, replacement_onCreate_action)

# 7. Update signature of scanCroppedArea
content = content.replace(
    "private fun scanCroppedArea(bitmap: Bitmap, x: Float, y: Float, w: Float, h: Float, shape: String) {",
    "private fun scanCroppedArea(bitmap: Bitmap, x: Float, y: Float, w: Float, h: Float, shape: String, points: List<Offset>) {"
)

# 8. Update signature of shareCroppedArea
content = content.replace(
    "private fun shareCroppedArea(bitmap: Bitmap, x: Float, y: Float, w: Float, h: Float, shape: String) {",
    "private fun shareCroppedArea(bitmap: Bitmap, x: Float, y: Float, w: Float, h: Float, shape: String, points: List<Offset>) {"
)

# 9. Update shareCroppedArea polygon clipping
target_share_clip = """            } else if (shape == "polygon") {
                val output = Bitmap.createBitmap(cropW, cropH, Bitmap.Config.ARGB_8888)
                val canvas = android.graphics.Canvas(output)
                canvas.drawColor(android.graphics.Color.WHITE)
                val path = android.graphics.Path()
                val cx = cropW / 2f
                val cy = cropH / 2f
                val rx = cropW / 2f
                val ry = cropH / 2f
                path.moveTo(cx, cy - ry)
                path.lineTo(cx + rx * 0.866f, cy - ry * 0.5f)
                path.lineTo(cx + rx * 0.866f, cy + ry * 0.5f)
                path.lineTo(cx, cy + ry)
                path.lineTo(cx - rx * 0.866f, cy + ry * 0.5f)
                path.lineTo(cx - rx * 0.866f, cy - ry * 0.5f)
                path.close()
                canvas.clipPath(path)
                canvas.drawBitmap(croppedBitmap, 0f, 0f, null)
                croppedBitmap = output
            }"""
replacement_share_clip = """            } else if (shape == "polygon") {
                val output = Bitmap.createBitmap(cropW, cropH, Bitmap.Config.ARGB_8888)
                val canvas = android.graphics.Canvas(output)
                canvas.drawColor(android.graphics.Color.WHITE)
                if (points.isNotEmpty()) {
                    val path = android.graphics.Path()
                    path.moveTo(points.first().x - startX, points.first().y - startY)
                    for (i in 1 until points.size) {
                        path.lineTo(points[i].x - startX, points[i].y - startY)
                    }
                    path.close()
                    canvas.clipPath(path)
                }
                canvas.drawBitmap(croppedBitmap, 0f, 0f, null)
                croppedBitmap = output
            }"""
content = content.replace(target_share_clip, replacement_share_clip)

# We must also do the same for scanCroppedArea if it uses the shape
target_scan_clip = """            if (shape == "circle") {
                val output = Bitmap.createBitmap(cropW, cropH, Bitmap.Config.ARGB_8888)
                val canvas = android.graphics.Canvas(output)
                canvas.drawColor(android.graphics.Color.WHITE)
                val path = android.graphics.Path()
                path.addOval(android.graphics.RectF(0f, 0f, cropW.toFloat(), cropH.toFloat()), android.graphics.Path.Direction.CW)
                canvas.clipPath(path)
                canvas.drawBitmap(croppedBitmap, 0f, 0f, null)
                croppedBitmap = output
            } else if (shape == "polygon") {
                val output = Bitmap.createBitmap(cropW, cropH, Bitmap.Config.ARGB_8888)
                val canvas = android.graphics.Canvas(output)
                canvas.drawColor(android.graphics.Color.WHITE)
                val path = android.graphics.Path()
                val cx = cropW / 2f
                val cy = cropH / 2f
                val rx = cropW / 2f
                val ry = cropH / 2f
                path.moveTo(cx, cy - ry)
                path.lineTo(cx + rx * 0.866f, cy - ry * 0.5f)
                path.lineTo(cx + rx * 0.866f, cy + ry * 0.5f)
                path.lineTo(cx, cy + ry)
                path.lineTo(cx - rx * 0.866f, cy + ry * 0.5f)
                path.lineTo(cx - rx * 0.866f, cy - ry * 0.5f)
                path.close()
                canvas.clipPath(path)
                canvas.drawBitmap(croppedBitmap, 0f, 0f, null)
                croppedBitmap = output
            }"""
replacement_scan_clip = """            if (shape == "circle") {
                val output = Bitmap.createBitmap(cropW, cropH, Bitmap.Config.ARGB_8888)
                val canvas = android.graphics.Canvas(output)
                canvas.drawColor(android.graphics.Color.WHITE)
                val path = android.graphics.Path()
                path.addOval(android.graphics.RectF(0f, 0f, cropW.toFloat(), cropH.toFloat()), android.graphics.Path.Direction.CW)
                canvas.clipPath(path)
                canvas.drawBitmap(croppedBitmap, 0f, 0f, null)
                croppedBitmap = output
            } else if (shape == "polygon") {
                val output = Bitmap.createBitmap(cropW, cropH, Bitmap.Config.ARGB_8888)
                val canvas = android.graphics.Canvas(output)
                canvas.drawColor(android.graphics.Color.WHITE)
                if (points.isNotEmpty()) {
                    val path = android.graphics.Path()
                    path.moveTo(points.first().x - startX, points.first().y - startY)
                    for (i in 1 until points.size) {
                        path.lineTo(points[i].x - startX, points[i].y - startY)
                    }
                    path.close()
                    canvas.clipPath(path)
                }
                canvas.drawBitmap(croppedBitmap, 0f, 0f, null)
                croppedBitmap = output
            }"""
content = content.replace(target_scan_clip, replacement_scan_clip)

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "w") as f:
    f.write(content)

