# Blueprint

## Active Tasks
- [x] Fix Notification History not saving all notifications.
  - Removed `isClearable` check from `AppNotificationListener` so that all notifications (including ongoing) are saved to history.
  - Added fallback parsing for `EXTRA_BIG_TEXT`, `EXTRA_SUB_TEXT`, and `tickerText` in case `EXTRA_TEXT` is missing.
- [x] Fix Notification Sidebar not hiding when opening history.
  - Added `onCloseSidebar()` to the History button click listener in `NotificationPageView`.

## Next Action
- Await further user instruction.
