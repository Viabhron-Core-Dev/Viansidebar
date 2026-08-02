2026-08-02T16:04:00Z
- Requested: Fix auto-scroll pause button not working and change the gesture position to the top half to avoid chatbot inputs in the bottom half.
- Modified: `AutoScrollManager.kt`
- Action:
  1. Modified gesture points: `startY` changed from `0.7f` to `0.5f` (starts exactly in the middle) and `endY` changed from `0.3f` to `0.15f` (ends at the top 15%, below notification bar). This completely limits the gesture to the top half of the screen.
  2. Fixed Pause logic: `btnPausePlay`'s click couldn't effectively cancel a long accessibility gesture because system dispatches can block or immediately restart if interrupted. Injected an `onCancelled` listener on the gesture. When the gesture is cancelled (e.g., by the user physically touching the screen to pause), it now automatically pauses the auto-scrolling (`isScrolling = false`) and updates the play icon to paused, instead of instantly restarting the gesture.
- Verified: Local build only (BUILD SUCCESSFUL).
