import sys

with open('app/src/main/java/com/example/WidgetPickerActivity.kt', 'r') as f:
    content = f.read()

target = """                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .clickable { onWidgetSelected(provider) }
                                        .padding(vertical = 12.dp, horizontal = 16.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {"""

replacement = """                                    val spanX = Math.ceil((provider.minWidth + 30) / 70.0).toInt()
                                    val spanY = Math.ceil((provider.minHeight + 30) / 70.0).toInt()
                                    val is1x1 = spanX <= 1 && spanY <= 1
                                    val isSidebar = actionType == "ADD_ELEMENT"
                                    val enabled = !isSidebar || is1x1
                                    
                                    Row(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .clickable(enabled = enabled) { onWidgetSelected(provider) }
                                            .padding(vertical = 12.dp, horizontal = 16.dp),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {"""

content = content.replace(target, replacement)

target2 = """                                    Column {
                                        Text(
                                            text = provider.loadLabel(pm),
                                            style = MaterialTheme.typography.bodyLarge,
                                            maxLines = 1,
                                            overflow = TextOverflow.Ellipsis
                                        )
                                    }"""

replacement2 = """                                    Column(modifier = Modifier.weight(1f)) {
                                        Text(
                                            text = provider.loadLabel(pm),
                                            style = MaterialTheme.typography.bodyLarge,
                                            color = if (enabled) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.onSurface.copy(alpha = 0.3f),
                                            maxLines = 1,
                                            overflow = TextOverflow.Ellipsis
                                        )
                                        Text(
                                            text = "${spanX}x${spanY}",
                                            style = MaterialTheme.typography.bodySmall,
                                            color = if (enabled) MaterialTheme.colorScheme.onSurfaceVariant else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.3f)
                                        )
                                    }"""

content = content.replace(target2, replacement2)

with open('app/src/main/java/com/example/WidgetPickerActivity.kt', 'w') as f:
    f.write(content)
