import re

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'r') as f:
    content = f.read()

# Replace 1
content = content.replace("""                            } catch (e: Exception) {
                                e.printStackTrace()
                            }
                        },
                        onLongClick""", """                            } catch (e: Exception) {
                                com.example.LogKeeper.writeLog("Notification", "Failed to open notification content for ${sbn.packageName}: ${e.message}")
                            }
                        },
                        onLongClick""")

# Replace 2
content = content.replace("""                                            } catch (e: Exception) {
                                                e.printStackTrace()
                                            }
                                        }
                                    },""", """                                            } catch (e: Exception) {
                                                com.example.LogKeeper.writeLog("Notification", "Failed to send reply to ${sbn.packageName}: ${e.message}")
                                            }
                                        }
                                    },""")
# Replace 3
content = content.replace("""                                                try {
                                                    action.actionIntent.send()
                                                } catch (e: Exception) {
                                                    e.printStackTrace()
                                                }
                                            },""", """                                                try {
                                                    action.actionIntent.send()
                                                } catch (e: Exception) {
                                                    com.example.LogKeeper.writeLog("Notification", "Failed to execute action ${actionTitle} for ${sbn.packageName}: ${e.message}")
                                                }
                                            },""")

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'w') as f:
    f.write(content)
