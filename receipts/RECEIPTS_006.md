2026-08-02T16:20:00Z
- Requested: Fix floating windows (pages, work notes, pwa loader, dictionary) being too big/going out of screen, and fix handle adjustment y position slider representing screen height instead of an arbitrary 0-2500 range.
- Modified: `PageWindowManager.kt`, `WorkNotesWindowManager.kt`, `DictionaryWindowManager.kt`, `PwaWindowManager.kt`, `FloatingReaderService.kt`, `HandleEditScreen.kt`
- Action:
  1. Updated `HandleEditScreen.kt`: Changed `valueRange = 0f..2500f` to `0f..100f` for the Y Position slider so it properly represents the 0-100% of the screen height expected by `TriggerHandleView.kt`.
  2. Updated Window Managers (`Page`, `WorkNotes`, `Dictionary`, `Pwa`) and `FloatingReaderService`: Replaced the hardcoded defaults of `800` (width) and `1000` (height) with dynamic dimensions `context.resources.displayMetrics.widthPixels * 0.85` and `heightPixels * 0.6`. This limits the initial and default un-fullscreen window sizes so they don't overflow small screens.
- Verified: Local build only (BUILD SUCCESSFUL).
