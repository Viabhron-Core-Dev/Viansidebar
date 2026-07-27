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
