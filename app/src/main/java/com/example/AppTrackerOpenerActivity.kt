package com.example

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.provider.Settings

class AppTrackerOpenerActivity : Activity() {
    private var packageNames = arrayListOf<String>()
    private var currentIndex = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        packageNames = intent.getStringArrayListExtra("packages") ?: arrayListOf()
        if (packageNames.isEmpty()) {
            finish()
            return
        }
        openNext()
    }

    private fun openNext() {
        if (currentIndex < packageNames.size) {
            val pkg = packageNames[currentIndex]
            currentIndex++
            try {
                val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
                    data = Uri.parse("package:$pkg")
                }
                startActivityForResult(intent, 100)
            } catch (e: Exception) {
                openNext()
            }
        } else {
            finish()
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 100) {
            openNext()
        }
    }
}
