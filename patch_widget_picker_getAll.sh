cat << 'INNER_EOF' > script.awk
/appWidgetManager = AppWidgetManager.getInstance\(this\)/ {
    print "        appWidgetManager = AppWidgetManager.getInstance(this)"
    print "        val allProviders = mutableListOf<AppWidgetProviderInfo>()"
    print "        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {"
    print "            val userManager = getSystemService(android.content.Context.USER_SERVICE) as android.os.UserManager"
    print "            for (profile in userManager.userProfiles) {"
    print "                allProviders.addAll(appWidgetManager.getInstalledProvidersForProfile(profile))"
    print "            }"
    print "        } else {"
    print "            allProviders.addAll(appWidgetManager.installedProviders)"
    print "        }"
    next
}
/providers = appWidgetManager.installedProviders/ {
    print "                    providers = allProviders,"
    print "                    actionType = intent.getStringExtra(\"ACTION_TYPE\") ?: \"\","
    next
}
{ print }
INNER_EOF
awk -f script.awk app/src/main/java/com/example/WidgetPickerActivity.kt > tmp.kt
mv tmp.kt app/src/main/java/com/example/WidgetPickerActivity.kt
