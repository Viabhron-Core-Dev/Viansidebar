import re

with open('app/src/main/java/com/example/service/QuickTileHandler.kt', 'r') as f:
    content = f.read()

content = content.replace(
    '"bluetooth" -> openSettings(context, Settings.ACTION_BLUETOOTH_SETTINGS)',
    '''"bluetooth" -> openPanelOrSettings(context, "android.settings.panel.action.BLUETOOTH", Settings.ACTION_BLUETOOTH_SETTINGS)
            "pair" -> openSettings(context, Settings.ACTION_BLUETOOTH_SETTINGS)'''
)

with open('app/src/main/java/com/example/service/QuickTileHandler.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content2 = f.read()

content2 = content2.replace(
    'SidebarItem.QuickTile("bluetooth", "Bluetooth", android.R.drawable.ic_menu_share),',
    'SidebarItem.QuickTile("bluetooth", "Bluetooth", android.R.drawable.ic_menu_share),\n    SidebarItem.QuickTile("pair", "Pair Device", android.R.drawable.ic_menu_add),'
)

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content2)
