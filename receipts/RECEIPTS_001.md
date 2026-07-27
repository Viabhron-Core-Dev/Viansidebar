2026-07-27T06:05:00-07:00
Requested: Fix Hybrid grid edit mode not saving properly to the floating view and folder edits not persisting.
Files touched:
- app/src/main/java/com/example/HybridGridEditActivity.kt
- app/src/main/java/com/example/WidgetsGridEditActivity.kt
- app/src/main/java/com/example/service/HybridGridPageView.kt
- app/src/main/java/com/example/service/WidgetsGridPageView.kt
- app/src/main/java/com/example/PageCustomizeScreen.kt
Details:
- Fixed a bug in `HybridGridEditActivity` where edited folders were incorrectly saving to `sidebar_hybrid_` instead of `hybrid_grid_`.
- Added an `UPDATE_GRID` broadcast to `onDestroy` in both `HybridGridEditActivity` and `WidgetsGridEditActivity` so that the FloatingReaderService views reload their grids after edit mode is closed.
- Updated `HybridGridPageView` and `WidgetsGridPageView` to listen for the `UPDATE_GRID` broadcast and reload widgets when it is received.
- Prevented a duplicate widget bug in `HybridGridEditActivity` by omitting `ELEMENT_ID` from the `ELEMENT_ADDED_TO_HYBRID` broadcast since the grid saves it before broadcasting.
- Added a conditional check in `PageCustomizeScreen` to render an "EDIT GRID" button for `hybrid_grid` pages, routing to `HybridGridEditActivity`.
Verified: Local build only.
2026-07-27T07:54:00-07:00
Requested: Change "SYSTEM / USER" toggle to "SYSTEM ONLY" / "USER ONLY" in App Tracker whitelist edit mode.
Files touched:
- app/src/main/java/com/example/AppTrackerSettingsActivity.kt
Details:
- Modified `WhitelistTab` in `AppTrackerSettingsActivity` to filter apps exclusively based on `showSystemApps` boolean (i.e. `it.isSystem == showSystemApps`), instead of showing both system and user apps when true.
- Changed the button text from "SYSTEM / USER" to "SYSTEM ONLY" to reflect this mutually exclusive toggle state.
Verified: Local build only.
2026-07-27T09:37:00-07:00
Requested: App tracker is showing apps that are already force stopped or not opened in Sidebar page app tracker running tab.
Files touched:
- app/src/main/java/com/example/service/AppTrackerPageView.kt
- app/src/main/java/com/example/AppTrackerSettingsActivity.kt
Details:
- Added a filter `if ((appInfo.flags and ApplicationInfo.FLAG_STOPPED) != 0) continue` to the running apps logic.
- This ensures apps that are explicitly force stopped by the system or user (or never launched since installation) are excluded from the recent apps list in both the sidebar tracker view and the settings whitelist config view.
Verified: Local build only.
2026-07-27T09:43:00-07:00
Requested: Widget added in widget grid edit mode not appearing in widget grid Sidebar page.
Files touched:
- app/src/main/java/com/example/service/WidgetsGridPageView.kt
- app/src/main/java/com/example/service/HybridGridPageView.kt
- app/src/main/java/com/example/WidgetsGridEditActivity.kt
- app/src/main/java/com/example/HybridGridEditActivity.kt
Details:
- Fixed a parsing bug where `wId` was being evaluated as `null` for new widgets. The `item.id` was formatted as `widget:ID:{json_string}`, and `id.removePrefix("widget:").toIntOrNull()` returned `null`.
- Updated all references to properly extract just the numeric ID portion using `.substringBefore(":")` before calling `.toIntOrNull()`.
Verified: Local build only.
2026-07-27T11:54:00-07:00
Requested: Widget that are 1x1 are appearing in 2x2.
Files touched:
- app/src/main/java/com/example/WidgetPickerActivity.kt
- app/src/main/java/com/example/WidgetsGridEditActivity.kt
- app/src/main/java/com/example/HybridGridEditActivity.kt
Details:
- Updated `WidgetPickerActivity` to calculate proper `cols` and `rows` using `targetCellWidth`/`targetCellHeight` (or falling back to `minWidth`/`minHeight` math) for widgets in `RETURN_ID` action and append it to the JSON string returned in `ELEMENT_ID`.
- Updated `WidgetsGridEditActivity` and `HybridGridEditActivity` to parse the `cols` and `rows` from the `ELEMENT_ID` JSON instead of defaulting to 2x2, properly supporting 1x1 or any other sized widgets.
Verified: Local build only.
