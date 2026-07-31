import re

def remove_from_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # Remove UI Refs that belong to Reader
    content = re.sub(r'    private lateinit var tvWindowTitle: TextView\n', '', content)
    content = re.sub(r'    private lateinit var tvContent: TextView\n', '', content)
    content = re.sub(r'    private lateinit var scrollView: ScrollView\n', '', content)
    content = re.sub(r'    private lateinit var tvProgress: TextView\n', '', content)
    content = re.sub(r'    private lateinit var toolbarContainer: View\n', '', content)
    content = re.sub(r'    private lateinit var bubbleIcon: TextView\n', '', content)
    content = re.sub(r'    private lateinit var windowContainer: View\n', '', content)
    content = re.sub(r'    private lateinit var topDragBar: View\n', '', content)
    
    # Remove reader states
    content = re.sub(r'    private var cameFromLibrary = false\n', '', content)
    content = re.sub(r'    private var currentBook: EpubBook\? = null\n', '', content)
    content = re.sub(r'    private var currentChapterIndex: Int = 0\n', '', content)
    content = re.sub(r'    private var chapterContent: String = ""\n', '', content)
    content = re.sub(r'    private var isFolded = true\n', '', content)
    content = re.sub(r'    private var librarySearchQuery: String = ""\n', '', content)
    
    # Remove overlays
    content = re.sub(r'    private var overlayLibrary: View\? = null\n', '', content)
    content = re.sub(r'    private var overlayChapters: View\? = null\n', '', content)
    content = re.sub(r'    private var overlayBookmarks: View\? = null\n', '', content)
    content = re.sub(r'    private var overlaySearch: View\? = null\n', '', content)
    content = re.sub(r'    private var overlaySearchResults: View\? = null\n', '', content)
    content = re.sub(r'    private var overlayNotes: View\? = null\n', '', content)
    
    # Remove reader lists
    content = re.sub(r'    private var listLibrary: androidx\.recyclerview\.widget\.RecyclerView\? = null\n', '', content)
    content = re.sub(r'    private var listChapters: androidx\.recyclerview\.widget\.RecyclerView\? = null\n', '', content)
    content = re.sub(r'    private var listBookmarks: androidx\.recyclerview\.widget\.RecyclerView\? = null\n', '', content)
    
    # Remove theme function body
    content = re.sub(r'        if \(!::windowContainer\.isInitialized\) return\n', '', content)
    content = re.sub(r'        val bgColor = if \(isDark\) android\.graphics\.Color\.parseColor\("#222222"\) else android\.graphics\.Color\.WHITE\n', '', content)
    content = re.sub(r'        val txColor = if \(isDark\) android\.graphics\.Color\.parseColor\("#DDDDDD"\) else android\.graphics\.Color\.BLACK\n', '', content)
    content = re.sub(r'        windowContainer\.setBackgroundColor\(bgColor\)\n', '', content)
    content = re.sub(r'        tvContent\.setTextColor\(txColor\)\n', '', content)
    content = re.sub(r'        overlayChapters\?\.setBackgroundColor\(bgColor\)\n', '', content)
    content = re.sub(r'        overlayLibrary\?\.setBackgroundColor\(bgColor\)\n', '', content)

    # Remove quick notes
    content = re.sub(r'        // --- Quick Notes Implementation ---\n', '', content)
    content = re.sub(r'    private lateinit var listNotes: androidx\.recyclerview\.widget\.RecyclerView\n', '', content)
    content = re.sub(r'    private lateinit var btnNotesBack: View\n', '', content)
    content = re.sub(r'    private lateinit var btnNotesAdd: View\n', '', content)
    content = re.sub(r'    private lateinit var btnNotesDelete: View\n', '', content)
    content = re.sub(r'    private lateinit var tvNotesTitle: android\.widget\.TextView\n', '', content)
    content = re.sub(r'    private var notesAdapter: NotesAdapter\? = null\n', '', content)
    content = re.sub(r'    private val selectedNotes = mutableSetOf<com\.example\.data\.QuickNote>\(\)\n', '', content)
    content = re.sub(r'    private var notesList = listOf<com\.example\.data\.QuickNote>\(\)\n', '', content)
    content = re.sub(r'    private var notesSearchQuery: String = ""\n', '', content)
    content = re.sub(r'    private val bookmarksList = mutableListOf<BookmarkItem>\(\)\n', '', content)

    # Remove other unused reader variables
    content = re.sub(r'    private var tts: TextToSpeech\? = null\n', '', content)
    content = re.sub(r'    private var isTtsReady = false\n', '', content)
    content = re.sub(r'    private var isSpeaking = false\n', '', content)
    content = re.sub(r'    private lateinit var btnTts: ImageView\n', '', content)
    content = re.sub(r'    // Auto Scroll State\n', '', content)
    content = re.sub(r'    private var isAutoScrolling = false\n', '', content)
    content = re.sub(r'    private val scrollHandler = Handler\(Looper\.getMainLooper\(\)\)\n', '', content)
    content = re.sub(r'    private var mediaSession: android\.media\.session\.MediaSession\? = null\n', '', content)
    content = re.sub(r'    private val scrollRunnable = object : Runnable \{\n        override fun run\(\) \{\n            if \(isAutoScrolling\) \{\n                scrollView\.smoothScrollBy\(0, 2\)\n                scrollHandler\.postDelayed\(this, 30\) // light speed modifier\n            \}\n        \}\n    \}\n', '', content)
    
    with open(path, 'w') as f:
        f.write(content)

remove_from_file('app/src/main/java/com/example/service/SidebarService.kt')
