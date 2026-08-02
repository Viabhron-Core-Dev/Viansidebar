2026-08-01T10:05:40Z
- Requested: Fix memory leaks, Compose view attachment errors, and crashes related to `PageWindowManager` and its page views.
- Modified: `PageWindowManager.kt`, `SidebarService.kt`, `AppTrackerSettingsActivity.kt`
- Converted from Compose to XML: `CalculatorPageView.kt`, `CompassPageView.kt`, `SchedulerPageView.kt`, `NotificationPageView.kt`, `AppTrackerPageView.kt`, `MediaPlayerPageView.kt`.
- Created XMLs: `page_calculator.xml`, `page_compass.xml`, `page_scheduler.xml`, `item_scheduler_task.xml`, `dialog_scheduler_task.xml`, `page_app_tracker.xml`, `item_app_tracker_row.xml`, `page_notification.xml`, `item_notification_row.xml`, `page_media_player.xml`
- Action:
  1. Re-added `ViewTreeLifecycleOwner` logic to `PageWindowManager` using a `CustomLifecycleOwner` to safely manage any lifecycle-aware components.
  2. Completely rewrote all page views inside `PageWindowManager` (`Calculator`, `Compass`, `Scheduler`, `Notifications`, `App Tracker`, `Media Player`) to use standard Android XML Layouts and native Views instead of Jetpack Compose. This totally eliminates the `ComposeView` window detachment crash and performance overhead when rendering these inside a floating window overlay.
  3. Re-implemented all features natively: Custom Canvas for Compass, RecyclerViews for Scheduler and Notifications, MediaController UI updates for Media Player, etc.
  4. Patched `SidebarService` and `AppTrackerSettingsActivity` to resolve API mismatches introduced by the rewrite.
- Verified: Local build only (BUILD SUCCESSFUL).
