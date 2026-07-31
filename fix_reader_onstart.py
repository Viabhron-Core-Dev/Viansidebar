import re

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'r') as f:
    content = f.read()

replacement = """    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val bookId = intent?.getIntExtra("BOOK_ID", -1) ?: -1
        val fromLauncher = intent?.getBooleanExtra("OPEN_FROM_LAUNCHER", false) ?: false
        val unfold = intent?.getBooleanExtra("UNFOLD", false) ?: false
        
        if (fromLauncher) {
            val lastBook = prefs.getInt("last_book_id", -1)
            if (lastBook != -1) {
                loadBook(lastBook)
                setFolded(false)
            } else {
                openLibraryView()
                setFolded(false)
            }
        } else if (bookId != -1) {
            loadBook(bookId)
            setFolded(false)
        } else if (unfold) {
            val lastBook = prefs.getInt("last_book_id", -1)
            if (currentBook == null && lastBook != -1) loadBook(lastBook)
            setFolded(false)
        }
        return START_NOT_STICKY
    }"""

content = re.sub(r'    override fun onStartCommand.*?return START_NOT_STICKY\n    \}', replacement, content, flags=re.DOTALL)

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'w') as f:
    f.write(content)
