with open("app/src/main/java/com/example/db/NotificationHistoryDao.kt", "r") as f:
    content = f.read()

target_dao = """    @Query("SELECT * FROM notification_history WHERE (title LIKE '%' || :query || '%' OR text LIKE '%' || :query || '%' OR appName LIKE '%' || :query || '%') AND packageName NOT IN (:excludedPackages) ORDER BY timestamp DESC")
    fun search(query: String, excludedPackages: List<String>): Flow<List<NotificationHistory>>"""

replacement_dao = """    @Query("SELECT * FROM notification_history WHERE (title LIKE '%' || :query || '%' OR text LIKE '%' || :query || '%' OR appName LIKE '%' || :query || '%') ORDER BY timestamp DESC")
    fun searchAll(query: String): Flow<List<NotificationHistory>>

    @Query("SELECT * FROM notification_history WHERE (title LIKE '%' || :query || '%' OR text LIKE '%' || :query || '%' OR appName LIKE '%' || :query || '%') AND packageName NOT IN (:excludedPackages) ORDER BY timestamp DESC")
    fun search(query: String, excludedPackages: List<String>): Flow<List<NotificationHistory>>"""

content = content.replace(target_dao, replacement_dao)

with open("app/src/main/java/com/example/db/NotificationHistoryDao.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/NotificationHistoryActivity.kt", "r") as f:
    content = f.read()

target_activity = """    LaunchedEffect(searchQuery, hiddenPackages) {
        if (searchQuery.isBlank()) {
            dao.getFiltered(hiddenPackages.toList()).collectLatest { history = it }
        } else {
            dao.search(searchQuery, hiddenPackages.toList()).collectLatest { history = it }
        }
    }"""

replacement_activity = """    LaunchedEffect(searchQuery, hiddenPackages) {
        if (searchQuery.isBlank()) {
            if (hiddenPackages.isEmpty()) {
                dao.getAll().collectLatest { history = it }
            } else {
                dao.getFiltered(hiddenPackages.toList()).collectLatest { history = it }
            }
        } else {
            if (hiddenPackages.isEmpty()) {
                dao.searchAll(searchQuery).collectLatest { history = it }
            } else {
                dao.search(searchQuery, hiddenPackages.toList()).collectLatest { history = it }
            }
        }
    }"""

content = content.replace(target_activity, replacement_activity)

with open("app/src/main/java/com/example/NotificationHistoryActivity.kt", "w") as f:
    f.write(content)
