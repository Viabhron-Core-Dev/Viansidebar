package com.example

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import java.net.URLEncoder

class ShortcutPickerActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val pickIntent = Intent(Intent.ACTION_PICK_ACTIVITY)
        pickIntent.putExtra(Intent.EXTRA_INTENT, Intent(Intent.ACTION_CREATE_SHORTCUT))
        pickIntent.putExtra(Intent.EXTRA_TITLE, "Select Shortcut")
        startActivityForResult(pickIntent, 100)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 100 && resultCode == Activity.RESULT_OK && data != null) {
            // Android gives us back an Intent to start the shortcut creation activity
            startActivityForResult(data, 101)
        } else if (requestCode == 101 && resultCode == Activity.RESULT_OK && data != null) {
            // Android gives us back the shortcut itself
            val intent = data.getParcelableExtra<Intent>(Intent.EXTRA_SHORTCUT_INTENT)
            val name = data.getStringExtra(Intent.EXTRA_SHORTCUT_NAME) ?: "Shortcut"
            
            if (intent != null) {
                val uri = intent.toUri(0)
                val encodedLabel = URLEncoder.encode(name, "UTF-8")
                val encodedUri = URLEncoder.encode(uri, "UTF-8")
                val id = "intent:$encodedLabel:$encodedUri"
                
                val resultIntent = Intent().apply { putExtra("ELEMENT_ID", id) }
                setResult(Activity.RESULT_OK, resultIntent)
                finish()
                return
            }
        }
        
        if (requestCode == 100 || requestCode == 101) {
            finish()
        }
    }
}
