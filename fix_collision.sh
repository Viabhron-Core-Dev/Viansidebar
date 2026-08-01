sed -i 's/handle_${handleId}_columns/handle_${handleId}_sidebar_columns/g' app/src/main/java/com/example/SidebarSettingsScreen.kt
sed -i 's/handle_${handleId}_width/handle_${handleId}_sidebar_width/g' app/src/main/java/com/example/SidebarSettingsScreen.kt
sed -i 's/handle_${handleId}_height/handle_${handleId}_sidebar_height/g' app/src/main/java/com/example/SidebarSettingsScreen.kt
sed -i 's/handle_${handleId}_wrap_content/handle_${handleId}_sidebar_wrap_content/g' app/src/main/java/com/example/SidebarSettingsScreen.kt
sed -i 's/handle_${handleId}_color/handle_${handleId}_sidebar_color/g' app/src/main/java/com/example/SidebarSettingsScreen.kt
sed -i 's/handle_${handleId}_transparency/handle_${handleId}_sidebar_transparency/g' app/src/main/java/com/example/SidebarSettingsScreen.kt

sed -i 's/handle_${containerId}_columns/handle_${containerId}_sidebar_columns/g' app/src/main/java/com/example/service/SidebarView.kt
sed -i 's/handle_${containerId}_width/handle_${containerId}_sidebar_width/g' app/src/main/java/com/example/service/SidebarView.kt
sed -i 's/handle_${containerId}_height/handle_${containerId}_sidebar_height/g' app/src/main/java/com/example/service/SidebarView.kt
sed -i 's/handle_${containerId}_wrap_content/handle_${containerId}_sidebar_wrap_content/g' app/src/main/java/com/example/service/SidebarView.kt
sed -i 's/handle_${containerId}_color/handle_${containerId}_sidebar_color/g' app/src/main/java/com/example/service/SidebarView.kt
sed -i 's/handle_${containerId}_transparency/handle_${containerId}_sidebar_transparency/g' app/src/main/java/com/example/service/SidebarView.kt

