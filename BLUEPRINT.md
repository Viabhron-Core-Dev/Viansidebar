# App Structure & Blueprint

## Recent Changes
- Grouped floating windows (eBook Reader, Dictionary Floating, PWA Loader, Floating Trigger) into a new "Floating Windows" category in the Add Element page.
- Created `WorkNotesWindowManager` for the Work Notes floating window, supporting minimize-to-bubble with a dynamic screenshot preview (`BubbleDrawable`).
- Refactored `SidebarAppsManager` to introduce `ALL_FLOATING_WINDOWS` for robust ID parsing across Grid, Trigger, and Sidebar.

## Current State
- The Add Element page now has cleaner categorizations: Special Items, Android Actions, and Floating Windows.
- The `SidebarAppsManager` provides parsed definitions for these floating windows which work across grid pages and the sidebar.
- Work Notes floating window is fully integrated, minimizing to a draggable bubble that restores its state when tapped.
- **Media Player Sidebar Page**: Added `MediaPlayerPageView` tracking active sessions from `MediaSessionManager`. Wraps content when present, and displays "Nothing playing" blank box when no active session.
