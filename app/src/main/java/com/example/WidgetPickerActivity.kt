package com.example

import android.app.Activity
import android.appwidget.AppWidgetManager
import android.content.Intent
import android.os.Bundle
import com.example.utils.AppWidgetHelper
import org.json.JSONObject

class WidgetPickerActivity : Activity() {

    private var appWidgetId = AppWidgetManager.INVALID_APPWIDGET_ID

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val host = AppWidgetHelper.getHost(this)
        appWidgetId = host.allocateAppWidgetId()
        
        val pickIntent = Intent(AppWidgetManager.ACTION_APPWIDGET_PICK)
        pickIntent.putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, appWidgetId)
        startActivityForResult(pickIntent, 100)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        
        if (resultCode == RESULT_OK && data != null) {
            val widgetId = data.getIntExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, appWidgetId)
            
            if (requestCode == 100) {
                // Widget selected, check if configuration is needed
                val widgetManager = AppWidgetManager.getInstance(this)
                val widgetInfo = widgetManager.getAppWidgetInfo(widgetId)
                
                if (widgetInfo != null && widgetInfo.configure != null) {
                    val configIntent = Intent(AppWidgetManager.ACTION_APPWIDGET_CONFIGURE)
                    configIntent.component = widgetInfo.configure
                    configIntent.putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, widgetId)
                    startActivityForResult(configIntent, 101)
                } else {
                    finishWithSuccess(widgetId)
                }
            } else if (requestCode == 101) {
                // Configuration done
                finishWithSuccess(widgetId)
            }
        } else {
            // Cancelled
            if (appWidgetId != AppWidgetManager.INVALID_APPWIDGET_ID) {
                AppWidgetHelper.getHost(this).deleteAppWidgetId(appWidgetId)
            }
            finish()
        }
    }
    
    private fun finishWithSuccess(widgetId: Int) {
        val actionType = intent.getStringExtra("ACTION_TYPE") ?: "ADD_ELEMENT"
        
        if (actionType == "ADD_ELEMENT") {
            val widgetManager = AppWidgetManager.getInstance(this)
            val info = widgetManager.getAppWidgetInfo(widgetId)
            val label = info?.loadLabel(packageManager) ?: "Widget"
            
            val json = JSONObject()
            json.put("widgetId", widgetId)
            json.put("label", label)
            val id = "widget:${widgetId}:${json.toString()}"
            
            val serviceIntent = Intent(this, com.example.service.FloatingReaderService::class.java)
            serviceIntent.action = "ADD_ELEMENT"
            serviceIntent.putExtra("element_id", id)
            
            val folderUuid = intent.getStringExtra("FOLDER_UUID")
            val isElementCallback = intent.getBooleanExtra("IS_ELEMENT_CALLBACK", false)
            
            if (folderUuid != null) {
                serviceIntent.putExtra("FOLDER_UUID", folderUuid)
            }
            if (isElementCallback) {
                serviceIntent.putExtra("IS_ELEMENT_CALLBACK", true)
            }
            startService(serviceIntent)
        } else if (actionType == "CREATE_PAGE") {
            // Send broadcast to PageManagementSettingsScreen
            val broadcastIntent = Intent("WIDGET_PAGE_CREATED")
            broadcastIntent.putExtra("WIDGET_ID", widgetId)
            sendBroadcast(broadcastIntent)
        }
        
        finish()
    }
}
