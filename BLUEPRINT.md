# VianSide Sidebar App Blueprint

## Overview
A highly customizable sidebar application providing quick access to apps, widgets, quick settings, and custom actions via an edge panel overlay.

## Development Phases
- [x] Implement core sidebar overlay service and touch detection
- [x] Build App Grid view with drag-and-drop and folder support
- [x] Build Hybrid Grid view for mixing widgets and apps
- [x] Synchronize Hybrid Grid folder popup styling and icon binding logic with App Grid
- [x] Resolve Utility action (Blue Light Filter) execution and icon state rendering across all grid types

## Recent Updates
- Fixed `DisplayHandler` preventing execution of `blue_light_filter` by improperly requiring `WRITE_SETTINGS` permission instead of relying solely on the application's existing overlay permission.
- Transferred `blue_light_filter` icon state rendering logic in `SidebarAppsManager` from `SystemAction` to `DisplayAction`.
- Extensively updated `HybridGridPageView` to support executing all system shortcuts, display actions, settings shortcuts, and volume/media controls (matching `AppsPageView`), along with a broadcast receiver to visually refresh toggle states without requiring a full sidebar reload.
