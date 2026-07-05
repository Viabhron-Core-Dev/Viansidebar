package com.example.service

import android.content.Context
import android.content.Intent
import android.hardware.camera2.CameraManager
import android.provider.Settings
import android.widget.Toast

object QuickTileHandler {
    private var isTorchOn = false

    fun handleQuickTileAction(context: Context, action: String) {
        when (action) {
            "torch" -> toggleTorch(context)
            "wifi" -> openSettings(context, Settings.ACTION_WIFI_SETTINGS)
            "bluetooth" -> openSettings(context, Settings.ACTION_BLUETOOTH_SETTINGS)
            "airplane" -> openSettings(context, Settings.ACTION_AIRPLANE_MODE_SETTINGS)
            "dnd" -> {
                try {
                    openSettings(context, Settings.ACTION_ZEN_MODE_PRIORITY_SETTINGS)
                } catch(e: Exception) {
                    openSettings(context, Settings.ACTION_SOUND_SETTINGS)
                }
            }
            "location" -> openSettings(context, Settings.ACTION_LOCATION_SOURCE_SETTINGS)
            "nfc" -> openSettings(context, Settings.ACTION_NFC_SETTINGS)
            "data" -> openSettings(context, Settings.ACTION_DATA_ROAMING_SETTINGS)
        }
    }

    private fun toggleTorch(context: Context) {
        try {
            val cameraManager = context.getSystemService(Context.CAMERA_SERVICE) as CameraManager
            val cameraId = cameraManager.cameraIdList[0]
            isTorchOn = !isTorchOn
            cameraManager.setTorchMode(cameraId, isTorchOn)
        } catch (e: Exception) {
            Toast.makeText(context, "Cannot access torch", Toast.LENGTH_SHORT).show()
        }
    }

    private fun openSettings(context: Context, action: String) {
        try {
            val intent = Intent(action)
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            context.startActivity(intent)
        } catch (e: Exception) {
            Toast.makeText(context, "Settings not available", Toast.LENGTH_SHORT).show()
        }
    }
}
