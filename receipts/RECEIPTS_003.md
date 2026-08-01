2026-07-27T23:43:00-07:00
Requested: Implement the fixes for the Force Stop app queue looping/crashing.
Files touched:
- app/src/main/res/xml/accessibility_service_config.xml
- app/src/main/java/com/example/service/VianSideAccessibilityService.kt
Action: Restored `canRetrieveWindowContent="true"` and the correct `accessibilityEventTypes` in the accessibility config. Updated `VianSideAccessibilityService` to correctly handle when an app is already force-stopped (button disabled) by pressing BACK, and added a BACK press after successfully clicking the OK confirmation button to ensure the queue loop continues to the next app.
Verification: Local build only.
2026-07-29T12:12:00-07:00
Requested: Fix home hybrid grid opening empty and big (wrap content) and restore Log Keeper and eBook Reader default elements.
Files touched: app/src/main/java/com/example/service/HybridGridPageView.kt, app/src/main/java/com/example/service/WidgetsGridPageView.kt, app/src/main/java/com/example/HybridGridEditActivity.kt, app/src/main/java/com/example/service/FloatingReaderService.kt
Action: Changed `getCurrentHeightPx` in `HybridGridPageView` and `WidgetsGridPageView` to return 0 when `gridLayout.childCount == 0` instead of a static 150dp padding, enabling them to wrap content tightly. Updated `getWidgetItems` and `loadHybridLocalItems` to check a new `hybrid_grid_modified_$pageId` flag, ensuring the default Log Keeper and eBook Reader elements are correctly populated unless the user explicitly saves a modified grid (which now flips the flag to true).
Verification: Local build

2026-08-01T08:12:00Z
Requested: Fix Floating Trigger toggle from sidebar, and make its executed action load the element properly.
Files touched:
- app/src/main/java/com/example/service/SidebarService.kt
- app/src/main/java/com/example/service/FloatingTriggerService.kt
Action: Added `floating_trigger:` intent handler in `SidebarService` to launch the `FloatingTriggerService` and toggle it when pressed from the sidebar. Rewrote `executeAction` in `FloatingTriggerService` to forward the `targetId` directly to `SidebarService.instance?.executeElementAction(targetId)`, enabling it to support all action types (Apps, PWAs, Widgets, Intent, Screen actions) gracefully instead of reimplementing a faulty/incomplete fallback logic.
Verification: Local build.
