2026-08-02T17:34:00Z
- Requested: Add Read Aloud functionality to floating dictionary window. Add settings cog in floating dictionary to navigate to Dictionary Settings. Enable font size scaling on dictionary definitions. Remove full screen dictionary component. Open floating dictionary with word selected from Context Menu via an OpenInNew icon. Parse HTML definition content.
- Modified: `DictionaryWindowManager.kt`, `layout_dictionary.xml`, `DictionarySettingsScreen.kt`, `DictionaryPopupActivity.kt`, `SidebarService.kt`, `AppsPageView.kt`, `SidebarAppsManager.kt`
- Action: 
  1. Updated `layout_dictionary.xml` to include `btn_settings` cog and remove `btn_speak_def` FAB. 
  2. Modified `DictionaryWindowManager.kt` to bind the settings cog to start `SettingsActivity` using the "dict" route. Set HTML parsing on `tvDefinition`. Configured dynamic text size scaling using `dict_font_size_scale` preferences. 
  3. Added `searchWord(query: String)` method to `DictionaryWindowManager` allowing the dictionary to seamlessly navigate to definitions when queried externally.
  4. Updated `DictionaryPopupActivity.kt` to present an `OpenInNew` icon which starts the `SidebarService` with `OPEN_DICTIONARY` action and the parsed query.
  5. Updated `SidebarService` `onStartCommand` to accept `OPEN_DICTIONARY` and forward to `dictWindowManager.searchWord()`.
  6. Added Font Size Scale Slider natively to `DictionarySettingsScreen.kt`.
  7. Globally purged `dictionary_full` references from `ActionPickerActivity`, `HybridGridPageView`, `AppsPageView`, `SidebarAppsManager`. 
- Verified: Local build only (BUILD SUCCESSFUL).
