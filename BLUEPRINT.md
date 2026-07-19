# Blueprint

## Active Tasks
- [x] Implement custom icon support in sidebar apps grid.
  - Added "Change Icon" and "Reset Icon" to long-press menu.
  - Created `IconPickerActivity` that launches image picker, crops image to square, adds 25% rounded corners with transparency, and saves it as WEBP to `custom_icons` folder.
  - Modified `AppsPageView` and `SidebarAppsManager` to prioritize loading these custom icons overriding default ones.
  - Broadcast updates to smoothly update UI immediately without restarting service.

## Next Action
- Await further user instruction.
