import re

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "r") as f:
    content = f.read()

# For grid elements
target1 = """                            elementView.setOnClickListener {
                                if (parsed is SidebarItem.App) {
                                    val intent = context.packageManager.getLaunchIntentForPackage(parsed.packageName)
                                    if (intent != null) {
                                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                        try { context.startActivity(intent) } catch (e: Exception) {}
                                    }
                                } else if (parsed is SidebarItem.Folder) {
                                    showFolderPopup(elementView, parsed, appsManager)
                                } else if (parsed is SidebarItem.PopupWidget) {
                                    showWidgetPopup(elementView, parsed)
                                } else if (parsed is SidebarItem.Link) {
                                    try {
                                        val intent = if (parsed.url.startsWith("intent:")) {
                                            Intent.parseUri(parsed.url, Intent.URI_INTENT_SCHEME)
                                        } else {
                                            Intent(Intent.ACTION_VIEW, android.net.Uri.parse(parsed.url))
                                        }
                                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                        context.startActivity(intent)
                                    } catch (e: Exception) {}
                                }
                            }"""

replacement1 = """                            elementView.setOnClickListener {
                                if (parsed is SidebarItem.App) {
                                    val intent = context.packageManager.getLaunchIntentForPackage(parsed.packageName)
                                    if (intent != null) {
                                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                        try { context.startActivity(intent) } catch (e: Exception) {}
                                    }
                                } else if (parsed is SidebarItem.Folder) {
                                    showFolderPopup(elementView, parsed, appsManager)
                                } else if (parsed is SidebarItem.PopupWidget) {
                                    showWidgetPopup(elementView, parsed)
                                } else if (parsed is SidebarItem.Link) {
                                    try {
                                        val intent = if (parsed.url.startsWith("intent:")) {
                                            Intent.parseUri(parsed.url, Intent.URI_INTENT_SCHEME)
                                        } else {
                                            Intent(Intent.ACTION_VIEW, android.net.Uri.parse(parsed.url))
                                        }
                                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                        context.startActivity(intent)
                                    } catch (e: Exception) {}
                                } else if (parsed is SidebarItem.QuickTile) {
                                    QuickTileHandler.handleQuickTileAction(context, parsed.action)
                                } else if (parsed is SidebarItem.IntentAction) {
                                    try {
                                        val intent = Intent.parseUri(parsed.uri, Intent.URI_INTENT_SCHEME)
                                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                        context.startActivity(intent)
                                    } catch (e: Exception) {}
                                } else if (parsed is SidebarItem.SystemAction) {
                                    if (parsed.action == "log_keeper") {
                                        val intent = Intent(context, com.example.LogKeeperActivity::class.java)
                                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                        context.startActivity(intent)
                                    } else if (parsed.action == "ebook_reader") {
                                        val intent = Intent(context, FloatingReaderService::class.java)
                                        intent.putExtra("UNFOLD", true)
                                        context.startService(intent)
                                    } else if (parsed.action == "screen_record") {
                                        val intent = Intent(context, ScreenRecordActivity::class.java)
                                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                        context.startActivity(intent)
                                    } else if (parsed.action == "settings") {
                                        val intent = Intent(context, com.example.SettingsActivity::class.java)
                                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                        context.startActivity(intent)
                                    } else {
                                        val service = VianSideAccessibilityService.instance
                                        if (service != null && service.performAction(parsed.action)) {
                                            com.example.LogKeeper.writeLog("Sidebar", "System action trigger: ${parsed.action}")
                                        } else {
                                            android.widget.Toast.makeText(context, "Please enable VianSide Accessibility Service", android.widget.Toast.LENGTH_SHORT).show()
                                            val intent = Intent(android.provider.Settings.ACTION_ACCESSIBILITY_SETTINGS)
                                            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                            try { context.startActivity(intent) } catch (e: Exception) {}
                                        }
                                    }
                                } else if (parsed is SidebarItem.VolumeAction) {
                                    try {
                                        MediaVolumeHandler.handleVolumeAction(context, parsed.stream, parsed.action)
                                    } catch (e: Exception) {}
                                } else if (parsed is SidebarItem.MediaAction) {
                                    try {
                                        MediaVolumeHandler.handleMediaAction(context, parsed.action)
                                    } catch (e: Exception) {}
                                } else if (parsed is SidebarItem.DisplayAction) {
                                    try {
                                        DisplayHandler.handleDisplayAction(context, parsed.action)
                                    } catch (e: Exception) {}
                                } else if (parsed is SidebarItem.SettingsShortcut) {
                                    try {
                                        SettingsShortcutHandler.handleSettingsShortcut(context, parsed.action)
                                    } catch (e: Exception) {}
                                }
                            }"""

content = content.replace(target1, replacement1)

# For folder popup
target2 = """                holder.itemView.setOnClickListener {
                    if (parsed is SidebarItem.App) {
                        val intent = context.packageManager.getLaunchIntentForPackage(parsed.packageName)
                        if (intent != null) {
                            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                            try { context.startActivity(intent) } catch (e: Exception) {}
                            popupWindow?.dismiss()
                        }
                    } else if (parsed is SidebarItem.Link) {
                        try {
                            val intent = if (parsed.url.startsWith("intent:")) {
                                Intent.parseUri(parsed.url, Intent.URI_INTENT_SCHEME)
                            } else {
                                Intent(Intent.ACTION_VIEW, android.net.Uri.parse(parsed.url))
                            }
                            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                            context.startActivity(intent)
                            popupWindow?.dismiss()
                        } catch (e: Exception) {}
                    }
                }"""
                
replacement2 = """                holder.itemView.setOnClickListener {
                    if (parsed is SidebarItem.App) {
                        val intent = context.packageManager.getLaunchIntentForPackage(parsed.packageName)
                        if (intent != null) {
                            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                            try { context.startActivity(intent) } catch (e: Exception) {}
                            popupWindow?.dismiss()
                        }
                    } else if (parsed is SidebarItem.Link) {
                        try {
                            val intent = if (parsed.url.startsWith("intent:")) {
                                Intent.parseUri(parsed.url, Intent.URI_INTENT_SCHEME)
                            } else {
                                Intent(Intent.ACTION_VIEW, android.net.Uri.parse(parsed.url))
                            }
                            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                            context.startActivity(intent)
                        } catch (e: Exception) {}
                        popupWindow?.dismiss()
                    } else if (parsed is SidebarItem.QuickTile) {
                        QuickTileHandler.handleQuickTileAction(context, parsed.action)
                        popupWindow?.dismiss()
                    } else if (parsed is SidebarItem.IntentAction) {
                        try {
                            val intent = Intent.parseUri(parsed.uri, Intent.URI_INTENT_SCHEME)
                            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                            context.startActivity(intent)
                        } catch (e: Exception) {}
                        popupWindow?.dismiss()
                    } else if (parsed is SidebarItem.SystemAction) {
                        if (parsed.action == "log_keeper") {
                            val intent = Intent(context, com.example.LogKeeperActivity::class.java)
                            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                            context.startActivity(intent)
                        } else if (parsed.action == "ebook_reader") {
                            val intent = Intent(context, FloatingReaderService::class.java)
                            intent.putExtra("UNFOLD", true)
                            context.startService(intent)
                        } else if (parsed.action == "screen_record") {
                            val intent = Intent(context, ScreenRecordActivity::class.java)
                            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                            context.startActivity(intent)
                        } else if (parsed.action == "settings") {
                            val intent = Intent(context, com.example.SettingsActivity::class.java)
                            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                            context.startActivity(intent)
                        } else {
                            val service = VianSideAccessibilityService.instance
                            if (service != null && service.performAction(parsed.action)) {
                                com.example.LogKeeper.writeLog("Sidebar", "System action trigger: ${parsed.action}")
                            } else {
                                android.widget.Toast.makeText(context, "Please enable VianSide Accessibility Service", android.widget.Toast.LENGTH_SHORT).show()
                                val intent = Intent(android.provider.Settings.ACTION_ACCESSIBILITY_SETTINGS)
                                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                try { context.startActivity(intent) } catch (e: Exception) {}
                            }
                        }
                        popupWindow?.dismiss()
                    } else if (parsed is SidebarItem.VolumeAction) {
                        try {
                            MediaVolumeHandler.handleVolumeAction(context, parsed.stream, parsed.action)
                        } catch (e: Exception) {}
                        popupWindow?.dismiss()
                    } else if (parsed is SidebarItem.MediaAction) {
                        try {
                            MediaVolumeHandler.handleMediaAction(context, parsed.action)
                        } catch (e: Exception) {}
                        popupWindow?.dismiss()
                    } else if (parsed is SidebarItem.DisplayAction) {
                        try {
                            DisplayHandler.handleDisplayAction(context, parsed.action)
                        } catch (e: Exception) {}
                        popupWindow?.dismiss()
                    } else if (parsed is SidebarItem.SettingsShortcut) {
                        try {
                            SettingsShortcutHandler.handleSettingsShortcut(context, parsed.action)
                        } catch (e: Exception) {}
                        popupWindow?.dismiss()
                    }
                }"""

content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "w") as f:
    f.write(content)
