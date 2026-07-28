import re

with open("app/src/main/java/com/example/service/AppTrackerPageView.kt", "r") as f:
    content = f.read()

target1 = """                val pm = context.packageManager
                val usm = context.getSystemService(Context.USAGE_STATS_SERVICE) as? UsageStatsManager
                val list = mutableListOf<TrackedAppInfo>()"""

replacement1 = """                val pm = context.packageManager
                val usm = context.getSystemService(Context.USAGE_STATS_SERVICE) as? UsageStatsManager
                val list = mutableListOf<TrackedAppInfo>()
                
                val homeIntent = Intent(Intent.ACTION_MAIN).apply {
                    addCategory(Intent.CATEGORY_HOME)
                }
                val launcherPkg = pm.resolveActivity(homeIntent, android.content.pm.PackageManager.MATCH_DEFAULT_ONLY)?.activityInfo?.packageName"""

content = content.replace(target1, replacement1)

target2 = """                    for ((pkgName, stat) in aggregated) {
                        if (stat.lastTimeUsed <= 0 || whitelistCurrent.contains(pkgName) || pkgName == context.packageName) continue"""

replacement2 = """                    for ((pkgName, stat) in aggregated) {
                        if (stat.lastTimeUsed <= 0 || whitelistCurrent.contains(pkgName) || pkgName == context.packageName || pkgName == launcherPkg) continue"""

content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/service/AppTrackerPageView.kt", "w") as f:
    f.write(content)
