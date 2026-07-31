2026-07-29T05:48:00-07:00
Requested: Hybrid/home grid. Edit mode is sometimes not working properly. Like columns arrangement doesn't get arranged properly. All works nice after reopen edit mode again. Check repo. just discuss no coding or building or updating blueprint.
Files touched: None
Action: Investigated grid edit modes. Found that `offsetX` and `offsetY` in `HybridGridEditActivity` and `WidgetsGridEditActivity` are cached in a `remember` block that lacks `cellWidthPx` and `cellHeightPx` as keys. This causes items to be stuck at (0,0) if the first layout pass has a 0 width constraint. Discussed findings with user.
Verification: Not tested - Discussion only
2026-07-29T06:01:00-07:00
Requested: Hybrid/home grid. Edit mode is sometimes not working properly. Like columns arrangement doesn't get arranged properly. All works nice after reopen edit mode again. Check repo. just discuss no coding or building or updating blueprint. (and then "Implement")
Files touched: `app/src/main/java/com/example/HybridGridEditActivity.kt`, `app/src/main/java/com/example/WidgetsGridEditActivity.kt`
Action: 
- Updated `remember` blocks for `offsetX` and `offsetY` inside `HybridGridEditActivity` and `WidgetsGridEditActivity`.
- Included `cellWidthPx` and `cellHeightPx` as cache keys in the `remember` block for both grids, allowing items to recalculate their actual layout offset when screen dimensions complete their first sizing pass, which resolves the bug where items are clumped together until a drag updates their state.
Verification: Verified by compiling Android code locally via Gradle. Build succeeded.
2026-07-31T00:36:00-07:00
Requested: Group floating windows inside Add Element page into a new section.
Touched: AddElementActivity.kt, SidebarAppsManager.kt
Action: Created a new "Floating Windows" category in `AddElementActivity`. Moved Floating Trigger, eBook Reader, Dictionary (Floating), and PWA Loader into this section. Removed eBook Reader and Dictionary (Floating) from the "Utilities" section in `SidebarAppsManager` as they are now top-level floating elements in the picker. Corrected request codes for Add Element selections (PWA Loader: 800, Floating Trigger: 700).
Verified: Compiled successfully.
2026-07-31T00:43:00-07:00
Requested: Special floating window for work notes and tracker. Topbar right corner settings page button, draggable topbar, minimize to bubble with last-state screenshot.
Touched: WorkNotesWindowManager.kt, WorkNotesService.kt, AndroidManifest.xml, AddElementActivity.kt, FloatingReaderService.kt, FloatingTriggerService.kt, HybridGridPageView.kt, SidebarAppsManager.kt
Action: Created `WorkNotesWindowManager` using `ComposeView` with `AndroidView` wrapper for the bubble. Implemented minimize-to-bubble by capturing a screenshot (`View.draw(Canvas(bitmap))`) and passing it to `BubbleDrawable`. Added the `work_notes` action to `SidebarAppsManager` (as part of a new `ALL_FLOATING_WINDOWS` list) so it parses correctly in `HybridGridPageView` and `FloatingTriggerService`. Bound the feature to `WorkNotesService` and registered it in `AndroidManifest.xml`.
Verified: Compiled successfully.
