import re

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'r') as f:
    content = f.read()

start_idx = content.find("@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)")
if start_idx == -1:
    start_idx = content.find("@OptIn(ExperimentalFoundationApi::class)")
end_idx = content.rfind("}")

new_code = """@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)
@Composable
fun NotificationItem(context: Context, sbn: StatusBarNotification, onHideApp: (String) -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    var replyText by remember { mutableStateOf("") }
    
    val notification = sbn.notification
    val title = notification.extras.getString(android.app.Notification.EXTRA_TITLE) ?: "No Title"
    val text = notification.extras.getCharSequence(android.app.Notification.EXTRA_TEXT)?.toString() ?: ""
    
    val pm = context.packageManager
    val appName = try {
        pm.getApplicationLabel(pm.getApplicationInfo(sbn.packageName, 0)).toString()
    } catch (e: Exception) {
        sbn.packageName
    }

    val dismissState = rememberSwipeToDismissBoxState(
        confirmValueChange = { dismissValue ->
            if (dismissValue == SwipeToDismissBoxValue.EndToStart || dismissValue == SwipeToDismissBoxValue.StartToEnd) {
                AppNotificationListener.instance?.cancelNotification(sbn.key)
                true
            } else {
                false
            }
        }
    )

    SwipeToDismissBox(
        state = dismissState,
        backgroundContent = {
            val color = when (dismissState.targetValue) {
                SwipeToDismissBoxValue.Settled -> Color.Transparent
                else -> Color.Red.copy(alpha = 0.5f)
            }
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(color, RoundedCornerShape(12.dp))
                    .padding(horizontal = 16.dp),
                contentAlignment = Alignment.CenterEnd
            ) {
                if (dismissState.targetValue != SwipeToDismissBoxValue.Settled) {
                    Text("Dismiss", color = Color.White)
                }
            }
        },
        content = {
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .combinedClickable(
                        onClick = {
                            expanded = !expanded
                        },
                        onLongClick = {
                            AppNotificationListener.instance?.cancelNotification(sbn.key)
                        }
                    ),
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = Color(0xFF2A2A2A))
            ) {
                Column(modifier = Modifier.padding(start = 12.dp, end = 12.dp, top = 8.dp, bottom = 12.dp)) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable {
                                try {
                                    notification.contentIntent?.send()
                                } catch (e: Exception) {
                                    e.printStackTrace()
                                }
                            }
                            .padding(bottom = 4.dp)
                    ) {
                        Text(
                            text = appName,
                            style = MaterialTheme.typography.labelSmall,
                            color = Color.LightGray,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.weight(1f)
                        )
                    }
                    
                    Text(
                        text = title,
                        style = MaterialTheme.typography.titleMedium,
                        color = Color.White,
                        maxLines = if (expanded) Int.MAX_VALUE else 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    
                    if (text.isNotEmpty()) {
                        Spacer(modifier = Modifier.height(2.dp))
                        Text(
                            text = text,
                            style = MaterialTheme.typography.bodyMedium,
                            color = Color.LightGray,
                            maxLines = if (expanded) Int.MAX_VALUE else 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                    
                    if (!expanded && (text.length > 30 || notification.actions?.isNotEmpty() == true)) {
                        Spacer(modifier = Modifier.height(4.dp))
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(2.dp)
                                .background(Color.Gray.copy(alpha = 0.5f), RoundedCornerShape(1.dp))
                        )
                    }
                    
                    if (expanded && notification.actions != null && notification.actions.isNotEmpty()) {
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        val remoteInputActions = notification.actions.filter { it.remoteInputs?.isNotEmpty() == true }
                        val normalActions = notification.actions.filter { it.remoteInputs.isNullOrEmpty() }
                        
                        if (remoteInputActions.isNotEmpty()) {
                            val replyAction = remoteInputActions.first()
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                OutlinedTextField(
                                    value = replyText,
                                    onValueChange = { replyText = it },
                                    placeholder = { Text(replyAction.title?.toString() ?: "Reply...") },
                                    modifier = Modifier.weight(1f),
                                    singleLine = true,
                                    textStyle = MaterialTheme.typography.bodyMedium.copy(color = Color.White)
                                )
                                Spacer(modifier = Modifier.width(8.dp))
                                Button(
                                    onClick = {
                                        if (replyText.isNotEmpty()) {
                                            try {
                                                val remoteInputs = replyAction.remoteInputs
                                                val intent = android.content.Intent()
                                                val bundle = android.os.Bundle()
                                                for (input in remoteInputs) {
                                                    bundle.putCharSequence(input.resultKey, replyText)
                                                }
                                                android.app.RemoteInput.addResultsToIntent(remoteInputs, intent, bundle)
                                                replyAction.actionIntent.send(context, 0, intent)
                                                replyText = ""
                                            } catch (e: Exception) {
                                                e.printStackTrace()
                                            }
                                        }
                                    },
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4CAF50))
                                ) {
                                    Text("Send")
                                }
                            }
                            Spacer(modifier = Modifier.height(8.dp))
                        }
                        
                        if (normalActions.isNotEmpty()) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                normalActions.take(3).forEach { action ->
                                    val actionTitle = action.title?.toString() ?: ""
                                    if (actionTitle.isNotEmpty()) {
                                        Button(
                                            onClick = {
                                                try {
                                                    action.actionIntent.send()
                                                } catch (e: Exception) {
                                                    e.printStackTrace()
                                                }
                                            },
                                            modifier = Modifier.weight(1f),
                                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF444444)),
                                            contentPadding = PaddingValues(horizontal = 8.dp, vertical = 4.dp)
                                        ) {
                                            Text(
                                                actionTitle,
                                                maxLines = 1,
                                                overflow = TextOverflow.Ellipsis,
                                                style = MaterialTheme.typography.labelSmall
                                            )
                                        }
                                    }
                                }
                            }
                        }
                    }
                    
                    if (expanded) {
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.End
                        ) {
                            TextButton(
                                onClick = { onHideApp(sbn.packageName) },
                                contentPadding = PaddingValues(horizontal = 8.dp, vertical = 4.dp)
                            ) {
                                Text("Hide App in Sidebar", style = MaterialTheme.typography.labelSmall, color = Color.Gray)
                            }
                        }
                    }
                }
            }
        }
    )
}
"""

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'w') as f:
    f.write(content[:start_idx] + new_code)
