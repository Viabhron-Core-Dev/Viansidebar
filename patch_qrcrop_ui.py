import re

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "r") as f:
    content = f.read()

target_screen = """@Composable
fun QRCropScreen(bitmap: Bitmap, onAction: (String, Float, Float, Float, Float) -> Unit, onClose: () -> Unit) {"""
replacement_screen = """@Composable
fun QRCropScreen(bitmap: Bitmap, onAction: (String, Float, Float, Float, Float, String) -> Unit, onClose: () -> Unit) {"""
content = content.replace(target_screen, replacement_screen)

target_ui = """            ) {
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
        }
        
        Row("""

replacement_ui = """            ) {
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
            }
        }
        
        Column(
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
        }
        
        Row("""

content = content.replace(target_ui, replacement_ui)

target_state = """    var cropRect by remember { mutableStateOf(Rect.Zero) }"""
replacement_state = """    var cropRect by remember { mutableStateOf(Rect.Zero) }
    var cropShape by remember { mutableStateOf("square") }"""
content = content.replace(target_state, replacement_state)

target_action1 = """onAction("share", realX, realY, realW, realH)"""
replacement_action1 = """onAction("share", realX, realY, realW, realH, cropShape)"""
content = content.replace(target_action1, replacement_action1)

target_action2 = """onAction("scan", realX, realY, realW, realH)"""
replacement_action2 = """onAction("scan", realX, realY, realW, realH, cropShape)"""
content = content.replace(target_action2, replacement_action2)

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "w") as f:
    f.write(content)
