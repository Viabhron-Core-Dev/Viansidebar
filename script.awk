/screenStateReceiver = object : android.content.BroadcastReceiver\(\) \{/ {
    print "        widgetPickerReceiver = object : android.content.BroadcastReceiver() {"
    print "            override fun onReceive(context: Context, intent: Intent) {"
    print "                if (intent.action == \"WIDGET_PICKER_CLOSED\") {"
    print "                    val pageId = intent.getStringExtra(\"PAGE_ID\")"
    print "                    if (pageId != null) {"
    print "                        showSidebar()"
    print "                        showWidgetsGridEditOverlay(pageId)"
    print "                    }"
    print "                }"
    print "            }"
    print "        }"
    print "        val widgetFilter = android.content.IntentFilter(\"WIDGET_PICKER_CLOSED\")"
    print "        registerReceiver(widgetPickerReceiver, widgetFilter, Context.RECEIVER_NOT_EXPORTED)"
    print ""
    print $0
    next
}
/private var screenStateReceiver/ {
    print "    private var widgetPickerReceiver: android.content.BroadcastReceiver? = null"
    print $0
    next
}
/screenStateReceiver\?\.let \{ unregisterReceiver\(it\) \}/ {
    print "        widgetPickerReceiver?.let { unregisterReceiver(it) }"
    print $0
    next
}
{ print }
