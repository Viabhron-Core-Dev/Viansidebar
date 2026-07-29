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
2026-07-28T15:04:00-07:00
Requested: Fix home grid not wrapping content correctly, and new handles opening sidebar on tap when no tap action is configured.
Files touched: app/src/main/java/com/example/service/FloatingReaderService.kt, app/src/main/java/com/example/utils/PageManager.kt, app/src/main/java/com/example/service/TriggerHandleView.kt
Action: Fixed `FloatingReaderService.kt` to dynamically query the height of `WidgetsGridPageView` and `HybridGridPageView` on initial creation, instead of defaulting to a hardcoded 450dp height which prevented the initial wrapContent state. Updated `PageManager.kt` to default `wrapContentHeight` to true for grid pages. Fixed `TriggerHandleView.kt` so tapping a trigger handle with a "none" gesture action no longer forcefully falls back to toggling the sidebar, preventing new handles from firing unintended actions when unconfigured.
Verification: Local build
2026-07-28T15:15:00-07:00
Requested: 1. Prevent adding widgets larger than grid columns. 2. Remove Dictionary and PWA Loader pages from add menu.
Files touched: app/src/main/java/com/example/WidgetsGridEditActivity.kt, app/src/main/java/com/example/HybridGridEditActivity.kt, app/src/main/java/com/example/SidebarSettingsScreen.kt, app/src/main/java/com/example/HandlesListSettingsScreen.kt, app/src/main/java/com/example/utils/PageManager.kt
Action: Added boundary check in `WidgetsGridEditActivity` and `HybridGridEditActivity` onActivityResult to show a Toast and cancel addition if the widget requires more columns than `totalCols`. Removed 'dictionary' and 'pwa_loader' from page dropdown options in SidebarSettingsScreen and HandlesListSettingsScreen, and filtered them out of page restoration and defaults.
Verification: Local build only
2026-07-28T15:20:00-07:00
Requested: Fix crash when moving or resizing widget "Cannot coerce value to an empty range: maximum -1 is less than minimum 0"
Files touched: app/src/main/java/com/example/HybridGridEditActivity.kt, app/src/main/java/com/example/WidgetsGridEditActivity.kt
Action: Added `maxOf(0, ...)` and `maxOf(1, ...)` wrappers around the maximum bound constraints in `coerceIn` for grid drag and resize actions in both grid editing activities. This ensures that the upper bound never drops below the lower bound, preventing the `IllegalArgumentException` from kotlin range constraints when dragging elements in highly constrained bounds or when column limits change.
Verification: Local build only
