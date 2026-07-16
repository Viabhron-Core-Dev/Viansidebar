#!/bin/bash
cat app/src/main/java/com/example/service/WidgetsGridPageView.kt | grep -A 20 "private fun getWidgetIds"
