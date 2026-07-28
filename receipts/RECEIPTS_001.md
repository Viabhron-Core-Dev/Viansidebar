2026-07-27T15:20:00-07:00
Requested: Fix invisible app icons in Hybrid Grid and make folder popup/icons identical to App Grid.
Files touched:
- app/src/main/java/com/example/service/SidebarAppsManager.kt
- app/src/main/java/com/example/service/HybridGridPageView.kt
Action: Extracted icon loading logic into a shared `bindIcon` helper method in `SidebarAppsManager` to properly load app, folder, and custom icons. Applied `bindIcon` to `HybridGridPageView` grid items and completely replaced the Hybrid Grid's folder popup implementation with a `RecyclerView` based layout that matches `AppsPageView` exactly, including long press context menus for "Remove", "Change Icon", etc.
Verification: Local build only.
