2026-07-27T15:27:00-07:00
Requested: Check the blue light filter in Sidebar add element utility. Not working.
Files touched:
- app/src/main/java/com/example/service/DisplayHandler.kt
- app/src/main/java/com/example/service/SidebarAppsManager.kt
- app/src/main/java/com/example/service/HybridGridPageView.kt
Action: Fixed `DisplayHandler` to not require `WRITE_SETTINGS` permission for `blue_light_filter` because it only uses overlay permission (which the sidebar already has). Moved the icon tinting logic for `blue_light_filter` in `SidebarAppsManager.kt` from `SystemAction` to `DisplayAction` where it belongs. Implemented click handling for all non-App/Link actions (like `DisplayAction`, `SettingsShortcut`, `QuickTile`, `VolumeAction`, etc.) in `HybridGridPageView`'s main grid items and folder popups to ensure functionality matches `AppsPageView`. Included handling for `com.example.UPDATE_SIDEBAR_ICONS` in `HybridGridPageView` to dynamically update the display of the toggle.
Verification: Local build only.
2026-07-27T15:35:00-07:00
Requested: App tracker tab while force stopping queue app info then my launcher crashed.
Files touched:
- app/src/main/java/com/example/service/AppTrackerPageView.kt
- app/src/main/java/com/example/service/VianSideAccessibilityService.kt
Action: Filtered out the default launcher package from the `recentApps` generation logic in `AppTrackerPageView` to prevent the user's home screen from crashing when "Force Stop All" is executed. Additionally, implemented the missing `onAccessibilityEvent` logic in `VianSideAccessibilityService` to properly identify and automatically click the "Force stop" and "OK" buttons when `isForceStopping` is active.
Verification: Local build only.
