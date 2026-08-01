package com.example.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun WindowBottomControls(
    onClose: () -> Unit,
    onMinimize: () -> Unit,
    onResize: (dx: Float, dy: Float) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .background(Color(0x88000000))
            .padding(2.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Close
        Box(
            modifier = Modifier
                .size(32.dp, 24.dp)
                .background(Color(0xFFF44336))
                .clickable { onClose() },
            contentAlignment = Alignment.Center
        ) {
            Icon(Icons.Default.Close, contentDescription = "Close", tint = Color.White, modifier = Modifier.size(16.dp))
        }
        
        Spacer(modifier = Modifier.width(8.dp))
        
        // Minimize
        Box(
            modifier = Modifier
                .size(32.dp, 24.dp)
                .background(Color(0xFF4CAF50))
                .clickable { onMinimize() },
            contentAlignment = Alignment.Center
        ) {
            Box(modifier = Modifier.size(12.dp, 2.dp).background(Color.White))
        }
        
        Spacer(modifier = Modifier.width(8.dp))
        
        // Resize
        Box(
            modifier = Modifier
                .size(32.dp, 24.dp)
                .background(Color(0xFF9E9E9E))
                .pointerInput(Unit) {
                    detectDragGestures { change, dragAmount ->
                        change.consume()
                        onResize(dragAmount.x, dragAmount.y)
                    }
                },
            contentAlignment = Alignment.Center
        ) {
            Text("///", color = Color.White, fontSize = 10.sp)
        }
    }
}
