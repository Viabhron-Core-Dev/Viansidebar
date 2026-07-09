package com.example.utils

import android.appwidget.AppWidgetHost
import android.content.Context

object AppWidgetHelper {
    const val HOST_ID = 10001
    private var _host: AppWidgetHost? = null

    fun getHost(context: Context): AppWidgetHost {
        if (_host == null) {
            _host = AppWidgetHost(context.applicationContext, HOST_ID)
            _host?.startListening()
        }
        return _host!!
    }
}
