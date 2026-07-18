import re

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "r") as f:
    content = f.read()

# Replace Canvas drawing to use Path FillType.EvenOdd
target_canvas = """            ) {
                // Dim background
                drawRect(Color.Black.copy(alpha = 0.5f))
                
                // Cutout center
                if (cropShape == "circle") {
                    drawOval(
                        color = Color.Transparent,
                        topLeft = cropRect.topLeft,
                        size = cropRect.size,
                        blendMode = androidx.compose.ui.graphics.BlendMode.Clear
                    )
                    // Draw border
                    drawOval(
                        color = Color.Green,
                        topLeft = cropRect.topLeft,
                        size = cropRect.size,
                        style = Stroke(width = 4.dp.toPx())
                    )
                } else {
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
                
                // Draw handles
                val hs = handleSize.toPx() / 2
                drawCircle(Color.Green, radius = hs, center = cropRect.topLeft)
                drawCircle(Color.Green, radius = hs, center = cropRect.topRight)
                drawCircle(Color.Green, radius = hs, center = cropRect.bottomLeft)
                drawCircle(Color.Green, radius = hs, center = cropRect.bottomRight)
            }"""

replacement_canvas = """            ) {
                val dimColor = Color.Black.copy(alpha = 0.5f)
                val path = androidx.compose.ui.graphics.Path().apply {
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
                drawCircle(Color.Green, radius = hs, center = cropRect.bottomRight)
            }"""
content = content.replace(target_canvas, replacement_canvas)

# Update the Column with proper icons/text
target_buttons = """        Column(
            modifier = Modifier
                .align(Alignment.CenterEnd)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            FloatingActionButton(onClick = { cropShape = "square" }, containerColor = if (cropShape == "square") Color.Green else Color.Gray) {
                Text("■")
            }
            FloatingActionButton(onClick = { cropShape = "circle" }, containerColor = if (cropShape == "circle") Color.Green else Color.Gray) {
                Text("●")
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
                Text("Hex", modifier = Modifier.padding(8.dp))
            }
        }"""
content = content.replace(target_buttons, replacement_buttons)

# Update crop image saving for polygon
target_share = """            if (shape == "circle") {
                val output = Bitmap.createBitmap(cropW, cropH, Bitmap.Config.ARGB_8888)
                val canvas = android.graphics.Canvas(output)
                canvas.drawColor(android.graphics.Color.WHITE)
                val path = android.graphics.Path()
                path.addOval(android.graphics.RectF(0f, 0f, cropW.toFloat(), cropH.toFloat()), android.graphics.Path.Direction.CW)
                canvas.clipPath(path)
                canvas.drawBitmap(croppedBitmap, 0f, 0f, null)
                croppedBitmap = output
            }"""
            
replacement_share = """            if (shape == "circle") {
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
content = content.replace(target_share, replacement_share)

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "w") as f:
    f.write(content)
