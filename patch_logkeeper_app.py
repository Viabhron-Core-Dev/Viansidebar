import re

with open("app/src/main/java/com/example/LogKeeper.kt", "r") as f:
    content = f.read()

target = """class App : Application() {
    override fun onCreate() {
        super.onCreate()
        LogKeeper.initialize(this)
    }
}"""

replacement = """class App : Application() {
    override fun onCreate() {
        super.onCreate()
        LogKeeper.initialize(this)
        
        val defaultHandler = Thread.getDefaultUncaughtExceptionHandler()
        Thread.setDefaultUncaughtExceptionHandler { thread, exception ->
            try {
                val stackTrace = android.util.Log.getStackTraceString(exception)
                LogKeeper.writeLog("CRASH", "FATAL EXCEPTION in thread ${thread.name}: ${exception.message}\\n$stackTrace")
            } catch (e: Exception) {
                android.util.Log.e("App", "Error writing crash log", e)
            }
            defaultHandler?.uncaughtException(thread, exception)
        }
    }
}"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/LogKeeper.kt", "w") as f:
    f.write(content)
