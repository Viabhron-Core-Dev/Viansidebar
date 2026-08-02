2026-08-02T12:12:00Z
- Requested: Long screenshot feature with floating UI (Start/Stop toggle, Speed, Split, and Pause/Resume). Stitch images by matching overlapping areas. Cache parts to disk first to preserve memory.
- Modified: `VianSideAccessibilityService.kt`, `SidebarAppsManager.kt`, Added `LongScreenshotManager.kt` and `overlay_long_screenshot.xml`
- Action: 
  1. Created `LongScreenshotManager` class running in the accessibility service context.
  2. Implemented `captureNextPart()` loop to take screenshots asynchronously and cache them as PNGs to disk.
  3. Implemented `scrollAndContinue()` using `GestureDescription` with variable speed controls.
  4. Built a pixel row matching algorithm in `findOverlap()` that compares rows of pixels to stitch images together precisely without creating duplicates of headers/footers.
  5. Built `overlay_long_screenshot.xml` providing Pause/Play, Split, Speed up, Speed down, and Exit controls.
  6. Added `long_screenshot` to `ALL_SCREEN_CAPTURE_ACTIONS` list in `SidebarAppsManager.kt`.
- Verified: Local build only (BUILD SUCCESSFUL).
