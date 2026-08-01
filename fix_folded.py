import os

files_data = {
    "app/src/main/java/com/example/service/PageWindowManager.kt": 'Text("P", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 24.sp)',
    "app/src/main/java/com/example/service/WorkNotesWindowManager.kt": 'Text("W", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 24.sp)',
    "app/src/main/java/com/example/service/PwaWindowManager.kt": 'Text("PWA", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 20.sp)'
}

for filepath, text_content in files_data.items():
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()

        # The folded view is inside 'val foldedComposeView = ComposeView(context).apply {'
        # and has an AndroidView with a background of BubbleDrawable(lastStateBitmap)
        # Let's replace the content inside the setContent { ... }
        
        # We find 'val foldedComposeView = ComposeView(context).apply {'
        # and replace up to 'setupLifecycle(foldedComposeView)'
        
        start_str = 'val foldedComposeView = ComposeView(context).apply {'
        end_str = 'setupLifecycle(foldedComposeView)'
        
        start_idx = content.find(start_str)
        if start_idx != -1:
            end_idx = content.find(end_str, start_idx)
            if end_idx != -1:
                replacement = f"""val foldedComposeView = ComposeView(context).apply {{
                setContent {{
                    MaterialTheme(colorScheme = darkColorScheme()) {{
                        Box(
                            modifier = Modifier
                                .size(64.dp)
                                .clip(CircleShape)
                                .background(Color(0xFF2A2A3C).copy(alpha = 0.9f))
                                .pointerInput(Unit) {{
                                    detectTapGestures(onTap = {{ unfold() }})
                                }}
                                .pointerInput(Unit) {{
                                    detectDragGestures {{ change, dragAmount ->
                                        change.consume()
                                        foldedLayoutParams?.x = (foldedLayoutParams?.x ?: 0) + dragAmount.x.roundToInt()
                                        foldedLayoutParams?.y = (foldedLayoutParams?.y ?: 0) + dragAmount.y.roundToInt()
                                        windowManager.updateViewLayout(this@apply, foldedLayoutParams)
                                    }}
                                }},
                            contentAlignment = Alignment.Center
                        ) {{
                            {text_content}
                        }}
                    }}
                }}
            }}
            """
                content = content[:start_idx] + replacement + content[end_idx:]
                
                with open(filepath, 'w') as f:
                    f.write(content)

