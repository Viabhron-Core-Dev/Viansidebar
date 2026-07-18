package com.example.service

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.unit.IntSize
import androidx.compose.ui.unit.dp
import com.example.LogKeeper
import com.google.zxing.BinaryBitmap
import com.google.zxing.MultiFormatReader
import com.google.zxing.RGBLuminanceSource
import com.google.zxing.common.HybridBinarizer
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.File

class QRCropActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val imagePath = intent.getStringExtra("IMAGE_PATH")
        if (imagePath == null) {
            Toast.makeText(this, "No image provided", Toast.LENGTH_SHORT).show()
            finish()
            return
        }

        val file = File(imagePath)
        if (!file.exists()) {
            Toast.makeText(this, "Image file not found", Toast.LENGTH_SHORT).show()
            finish()
            return
        }

        val bitmap = BitmapFactory.decodeFile(file.absolutePath)
        if (bitmap == null) {
            Toast.makeText(this, "Failed to load image", Toast.LENGTH_SHORT).show()
            finish()
            return
        }

        setContent {
            MaterialTheme(colorScheme = darkColorScheme()) {
                Surface(modifier = Modifier.fillMaxSize(), color = Color.Black) {
                    QRCropScreen(
                        bitmap = bitmap,
                        onAction = { action, x, y, width, height ->
                            if (action == "scan") {
                                scanCroppedArea(bitmap, x, y, width, height)
                            } else if (action == "share") {
                                shareCroppedArea(bitmap, x, y, width, height)
                            }
                        },
                        onClose = { finish() }
                    )
                }
            }
        }
    }

    private fun shareCroppedArea(bitmap: Bitmap, x: Float, y: Float, w: Float, h: Float) {
        val cropX = maxOf(0, x.toInt())
        val cropY = maxOf(0, y.toInt())
        val cropW = minOf(bitmap.width - cropX, w.toInt())
        val cropH = minOf(bitmap.height - cropY, h.toInt())
        if (cropW <= 0 || cropH <= 0) {
            Toast.makeText(this, "Invalid crop area", Toast.LENGTH_SHORT).show()
            return
        }
        try {
            val croppedBitmap = Bitmap.createBitmap(bitmap, cropX, cropY, cropW, cropH)
            val cacheFile = java.io.File(cacheDir, "shared_crop_${System.currentTimeMillis()}.png")
            java.io.FileOutputStream(cacheFile).use { out ->
                croppedBitmap.compress(Bitmap.CompressFormat.PNG, 100, out)
            }
            val uri = androidx.core.content.FileProvider.getUriForFile(this, "${packageName}.provider", cacheFile)
            val shareIntent = Intent(Intent.ACTION_SEND).apply {
                type = "image/png"
                putExtra(Intent.EXTRA_STREAM, uri)
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            }
            startActivity(Intent.createChooser(shareIntent, "Share Image"))
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(this, "Error sharing image", Toast.LENGTH_SHORT).show()
        }
    }

    private fun scanCroppedArea(bitmap: Bitmap, x: Float, y: Float, w: Float, h: Float) {
        val cropX = maxOf(0, x.toInt())
        val cropY = maxOf(0, y.toInt())
        val cropW = minOf(bitmap.width - cropX, w.toInt())
        val cropH = minOf(bitmap.height - cropY, h.toInt())

        if (cropW <= 0 || cropH <= 0) {
            Toast.makeText(this, "Invalid crop area", Toast.LENGTH_SHORT).show()
            return
        }

        val croppedBitmap = Bitmap.createBitmap(bitmap, cropX, cropY, cropW, cropH)
        
        Thread {
            try {
                val pixels = IntArray(cropW * cropH)
                croppedBitmap.getPixels(pixels, 0, cropW, 0, 0, cropW, cropH)
                val source = RGBLuminanceSource(cropW, cropH, pixels)
                val binaryBitmap = BinaryBitmap(HybridBinarizer(source))
                val reader = MultiFormatReader()
                val result = reader.decode(binaryBitmap)
                val text = result.text
                
                runOnUiThread {
                    if (text.isNullOrEmpty()) {
                        Toast.makeText(this, "No QR Code found in this area", Toast.LENGTH_SHORT).show()
                    } else {
                        LogKeeper.writeLog("QRCropActivity", "Successfully scanned QR Code: ${text.take(20)}...")
                        showResultDialog(text)
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
                runOnUiThread {
                    Toast.makeText(this, "No QR Code found", Toast.LENGTH_SHORT).show()
                }
            }
        }.start()
    }

    private fun showResultDialog(text: String) {
        setContent {
            MaterialTheme(colorScheme = darkColorScheme()) {
                AlertDialog(
                    onDismissRequest = { finish() },
                    title = { Text("Scanned QR Code (Secure)") },
                    text = { 
                        Column {
                            Text("Data treated with caution. Do not open unknown links.", style = MaterialTheme.typography.labelSmall, color = Color.Yellow)
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(text) 
                        }
                    },
                    confirmButton = {
                        TextButton(onClick = {
                            val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                            val clip = ClipData.newPlainText("QR Code", text)
                            clipboard.setPrimaryClip(clip)
                            Toast.makeText(this@QRCropActivity, "Copied to clipboard", Toast.LENGTH_SHORT).show()
                        }) {
                            Text("Copy Data")
                        }
                    },
                    dismissButton = {
                        if (text.startsWith("http://") || text.startsWith("https://")) {
                            TextButton(onClick = {
                                val intent = Intent(Intent.ACTION_VIEW, Uri.parse(text))
                                startActivity(intent)
                                finish()
                            }) {
                                Text("Open Link", color = Color.Red)
                            }
                        } else {
                            TextButton(onClick = { finish() }) {
                                Text("Close")
                            }
                        }
                    }
                )
            }
        }
    }
}

@Composable
fun QRCropScreen(bitmap: Bitmap, onAction: (String, Float, Float, Float, Float) -> Unit, onClose: () -> Unit) {
    var viewSize by remember { mutableStateOf(IntSize.Zero) }
    var cropRect by remember { mutableStateOf(Rect.Zero) }
    
    Box(modifier = Modifier.fillMaxSize().onSizeChanged { size ->
        viewSize = size
        if (cropRect == Rect.Zero && size.width > 0 && size.height > 0) {
            val boxSize = size.width * 0.6f
            cropRect = Rect(
                offset = Offset((size.width - boxSize) / 2f, (size.height - boxSize) / 2f),
                size = Size(boxSize, boxSize)
            )
        }
    }) {
        Image(
            bitmap = bitmap.asImageBitmap(),
            contentDescription = "Screenshot",
            modifier = Modifier.fillMaxSize(),
            contentScale = ContentScale.Fit
        )
        
        if (viewSize.width > 0) {
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
        }
        
        Row(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .fillMaxWidth()
                .background(Color.Black.copy(alpha = 0.7f))
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            Button(onClick = onClose, colors = ButtonDefaults.buttonColors(containerColor = Color.Gray)) {
                Text("Cancel")
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
            }
        }
    }
}
