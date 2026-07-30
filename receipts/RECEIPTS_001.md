2026-07-27T15:20:00-07:00
Requested: Fix invisible app icons in Hybrid Grid and make folder popup/icons identical to App Grid.
Files touched:
- app/src/main/java/com/example/service/SidebarAppsManager.kt
- app/src/main/java/com/example/service/HybridGridPageView.kt
Action: Extracted icon loading logic into a shared `bindIcon` helper method in `SidebarAppsManager` to properly load app, folder, and custom icons. Applied `bindIcon` to `HybridGridPageView` grid items and completely replaced the Hybrid Grid's folder popup implementation with a `RecyclerView` based layout that matches `AppsPageView` exactly, including long press context menus for "Remove", "Change Icon", etc.
Verification: Local build only.
2026-07-28T12:24:00-07:00
Requested: Fix App Tracker layout collapse and implement Force Stop queue bypass
Files touched: app/src/main/java/com/example/service/SidebarView.kt, app/src/main/java/com/example/service/VianSideAccessibilityService.kt
Action: Set wrapContent to false for app_tracker in SidebarView.kt to prevent height collapsing during load. Refactored VianSideAccessibilityService.kt to detect when "Force stop" becomes disabled (user manual click) and fire BACK to advance queue.
Verification: Local build
2026-07-28T12:34:00-07:00
Requested: Fix widget cropping and cramping in HybridGrid, WidgetsGrid, and Widget pages
Files touched: app/src/main/java/com/example/service/HybridGridPageView.kt, app/src/main/java/com/example/service/WidgetsGridPageView.kt, app/src/main/java/com/example/service/WidgetPageView.kt
Action: Added hostView.setPadding(0, 0, 0, 0) to remove default system widget padding. Also added updateAppWidgetSize() calls with proper layout dimensions to WidgetsGridPageView and WidgetPageView (and HybridGridPageView popup window) so widgets know exactly how much space they have.
Verification: Local build
2026-07-28T12:43:00-07:00
Requested: Add dictionary settings to main list, remove from sidebar page options, and label context menu as Meaning
Files touched: app/src/main/java/com/example/SettingsActivity.kt, app/src/main/java/com/example/PageManagementSettingsScreen.kt, app/src/main/AndroidManifest.xml
Action: Added "dict" route to MainSettingsScreen. Removed "dictionary" from the types list in PageManagementSettingsScreen. Added android:label="Meaning" to DictionaryPopupActivity in AndroidManifest.xml.
Verification: Local build
2026-07-28T12:52:30-07:00
Requested: Fix unnecessary background processing and crashes in App Tracker, Widgets Grid, and Hybrid Grid sidebar pages.
Files touched: app/src/main/java/com/example/service/HybridGridPageView.kt, app/src/main/java/com/example/service/WidgetsGridPageView.kt, app/src/main/java/com/example/service/AppTrackerPageView.kt
Action: Replaced the infinite recursive layout width checking loop (post { loadWidgets() }) with a zero-cost onSizeChanged override in both Grid pages to stop main thread flooding. Removed mass up-front application icon loading from the background data aggregation threads in App Tracker. Refactored App Tracker icon rendering to load lazily via Jetpack Compose LaunchedEffect, dramatically reducing memory usage and preventing OOM crashes.
Verification: Local build
2026-07-28T13:00:10-07:00
Requested: Fix Blue filter toggle icon not updating immediately in sidebar grids.
Files touched: app/src/main/java/com/example/service/HybridGridPageView.kt
Action: Added handling for "com.example.UPDATE_SIDEBAR_ICONS" broadcast in the HybridGridPageView's receiver to trigger an immediate UI reload (loadWidgets()) when the blue light filter is toggled, syncing the visual state instantly.
Verification: Local build
2026-07-28T13:07:30-07:00
Requested: Move utilities (blue light filter, log keeper, floating/full screen dictionary, ebook reader) into their own ActionPicker page like Screen Capture.
Files touched: app/src/main/java/com/example/service/SidebarAppsManager.kt, app/src/main/java/com/example/ActionPickerActivity.kt, app/src/main/java/com/example/AddElementActivity.kt
Action: Created a dedicated `ALL_UTILITIES_ACTIONS` list in `SidebarAppsManager` (and removed them from system/display lists). Registered the `"utilities"` category mapping in `ActionPickerActivity.kt` so it renders as a standalone page. Replaced the scattered flat buttons in `AddElementActivity.kt` with a single "Utilities" category button under "Android actions" that opens the new utilities picker.
Verification: Local build
2026-07-28T13:16:00-07:00
Requested: Migrate PWA Loader element from an AlertDialog popup to a full-screen page.
Files touched: app/src/main/AndroidManifest.xml, app/src/main/java/com/example/AddElementActivity.kt, app/src/main/java/com/example/PwaPickerActivity.kt
Action: Created `PwaPickerActivity.kt` as a full-screen RecyclerView that queries `PwaDatabase` for all PWAs and allows selection. Registered it in AndroidManifest.xml. Updated `AddElementActivity.kt` to launch `PwaPickerActivity` instead of running a local database query and popping an AlertDialog.
Verification: Local build
2026-07-28T13:27:00-07:00
Requested: Change the default sidebar page from Apps Grid to Hybrid Grid.
Files touched: app/src/main/java/com/example/utils/PageManager.kt, app/src/main/java/com/example/service/FloatingReaderService.kt
Action: Modified `PageManager.kt` to enforce `default_hybrid` (type: `hybrid_grid`) as the default first page instead of `default_apps`. Kept `default_apps` untouched in existing preferences so users don't lose data. Updated `ADD_ELEMENT` logic in `FloatingReaderService.kt` to dynamically look up the first page and properly write to the `hybrid_grid` JSON store (with default sizes of 2x2 for widgets and 1x1 for apps/shortcuts) instead of hardcoding `SidebarAppsManager` to `default_apps`.
Verification: Local build
2026-07-28T13:41:00-07:00
Requested: Fix trigger handle gestures (only tap worked) and ensure sidebar pops out from the edge matching the handle configuration.
Files touched: app/src/main/java/com/example/service/TriggerHandleView.kt, app/src/main/java/com/example/service/SidebarView.kt, app/src/main/java/com/example/service/FloatingReaderService.kt
Action: Added `override fun onDown(e: MotionEvent): Boolean { return true }` to `TriggerHandleView.kt`'s `GestureDetector` to enable tracking of swipe/fling gestures. Updated `SidebarView.kt` constructor to accept `handleId` and replaced the hardcoded `sidebar_position_left` check with `prefs.getString("handle_${handleId}_edge", "right") == "right"` (falling back to legacy prefs if `handleId == "sidebar"`). Updated `FloatingReaderService.kt` to pass `handleId` during `SidebarView` instantiations, including updating `showStandalonePage` to receive the `handleId` argument.
Verification: Local build
2026-07-28T14:00:20-07:00
Requested: Handle Management Screen Gestures (Expand Click Area)
Files touched: app/src/main/java/com/example/HandlesListSettingsScreen.kt
Action: Modified `onClick` condition for gestures in `HandlesListSettingsScreen.kt` to include `action.startsWith("open_page:")`, routing all page interactions directly to the Sidebar settings page instead of just the default `toggle_sidebar`.
Verification: Local build
2026-07-28T14:17:00-07:00
Requested: Make ereader and log keeper elements default elements in Sidebar page home(or default or hybrid grid).
Files touched: app/src/main/java/com/example/service/HybridGridPageView.kt
Action: Added fallback logic in `HybridGridPageView` so that if `hybrid_grid_$pageId` is unset and the page is `default_hybrid` (the home grid), it initializes with the E-Reader and Log Keeper system tools instead of an empty array.
Verification: Local build
2026-07-28T14:47:00-07:00
Requested: Fix hybrid grid edit mode not saving to sidebar page properly and prevent hybrid grid from being forced as a non-changeable default page.
Files touched: app/src/main/java/com/example/service/HybridGridPageView.kt, app/src/main/java/com/example/HybridGridEditActivity.kt, app/src/main/java/com/example/utils/PageManager.kt
Action: Made `default_hybrid` page unique to each handle (`default_hybrid_$handleId`) so they do not share layouts incorrectly. Removed logic in `PageManager` that forced the default grid to always persist, allowing the user to delete it if they want. Refactored `HybridGridEditActivity` to use a central `loadHybridLocalItems` function that properly falls back to default layout if empty, fixing the issue where saving an unedited default layout resulted in an empty grid being saved.
Verification: Local build
2026-07-30T01:05:00-07:00
Fixed compilation errors and finished migrating sidebar config to use handle-specific preferences.
Files modified:
- app/src/main/java/com/example/service/FloatingReaderService.kt
- app/src/main/java/com/example/service/SidebarView.kt
- app/src/main/java/com/example/service/AppsPageView.kt
- app/src/main/java/com/example/SidebarSettingsScreen.kt
- app/src/main/java/com/example/SidebarEditActivity.kt
Details:
- Used `containerId` (`{handleId}_{gesture}`) as the key prefix for `width`, `height`, `wrap_content`, `color`, `transparency`, `columns`, and `rows`.
- Fall back correctly to original `sidebar_` configurations if the handle-specific ones are not set.
- Ensured physical `handleId` is correctly passed to `SidebarView` so `isRight` still functions correctly and positions the view accurately on the left or right edges.
- Fixed `FloatingReaderService.kt` compile issues.
Verified via: `gradle :app:assembleDebug`
2026-07-30T01:05:00-07:00
Fixed compilation errors and finished migrating sidebar config to use handle-specific preferences.
Files modified:
- app/src/main/java/com/example/service/FloatingReaderService.kt
- app/src/main/java/com/example/service/SidebarView.kt
- app/src/main/java/com/example/service/AppsPageView.kt
- app/src/main/java/com/example/SidebarSettingsScreen.kt
- app/src/main/java/com/example/SidebarEditActivity.kt
Details:
- Used `containerId` (`{handleId}_{gesture}`) as the key prefix for `width`, `height`, `wrap_content`, `color`, `transparency`, `columns`, and `rows`.
- Fall back correctly to original `sidebar_` configurations if the handle-specific ones are not set.
- Ensured physical `handleId` is correctly passed to `SidebarView` so `isRight` still functions correctly and positions the view accurately on the left or right edges.
- Fixed `FloatingReaderService.kt` compile issues.
Verified via: `gradle :app:assembleDebug`
