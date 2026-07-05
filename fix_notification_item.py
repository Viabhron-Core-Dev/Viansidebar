import re

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'r') as f:
    content = f.read()

old_code = """@OptIn(ExperimentalFoundationApi::class)
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
    
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .combinedClickable(
                onClick = {
                    if (!expanded) {
                        expanded = true
                    } else {
                        try {
                            notification.contentIntent?.send()
                        } catch (e: Exception) {
                            e.printStackTrace()
                        }
                    }
                },
                onLongClick = {
                    AppNotificationListener.instance?.cancelNotification(sbn.key)
                }
            ),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF2A2A2A))
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {"""

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
                    ) {"""

content = content.replace(old_code, new_code)

old_code2 = """                    }
                }
            }
        }
    }
}"""

new_code2 = """                    }
                }
            }
        }
    })
}"""

content = content.replace(old_code2, new_code2)

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'w') as f:
    f.write(content)
