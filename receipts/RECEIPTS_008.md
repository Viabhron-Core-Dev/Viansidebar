2026-08-02T17:10:00Z
- Requested: Parse HTML tags in dictionary popup (from text selection context menu) and add a "Read Aloud" button for the word using system TTS.
- Modified: `DictionaryPopupActivity.kt`
- Action:
  1. Wrapped the dictionary definition text within an `AndroidView` returning a `TextView` to leverage `HtmlCompat.fromHtml`, correctly formatting paragraphs, italics, line breaks, and ordered lists.
  2. Implemented `TextToSpeech` (Android System TTS) in `DictionaryPopupActivity` to speak the selected word upon clicking a new `PlayArrow` icon button positioned next to the word. 
- Verified: Local build only (BUILD SUCCESSFUL).
