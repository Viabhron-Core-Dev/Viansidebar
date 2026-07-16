package com.example

import android.app.Activity
import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.view.Gravity
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import androidx.activity.ComponentActivity
import java.net.URLEncoder

class IntentPickerActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutParams = ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
            setBackgroundColor(Color.BLACK)
            setPadding(32, 32, 32, 32)
        }
        
        val title = TextView(this).apply {
            text = "Custom Intent"
            setTextColor(Color.WHITE)
            textSize = 20f
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, 16)
        }
        layout.addView(title)
        
        val editLabel = EditText(this).apply {
            hint = "Label (e.g., Open Website)"
            setHintTextColor(Color.GRAY)
            setTextColor(Color.WHITE)
        }
        layout.addView(editLabel)
        
        val editUri = EditText(this).apply {
            hint = "Intent URI (e.g., https://google.com)"
            setHintTextColor(Color.GRAY)
            setTextColor(Color.WHITE)
        }
        layout.addView(editUri)
        
        val btnSave = Button(this).apply {
            text = "Save"
            setOnClickListener {
                val label = editLabel.text.toString().trim()
                val uri = editUri.text.toString().trim()
                if (label.isNotEmpty() && uri.isNotEmpty()) {
                    val encodedLabel = URLEncoder.encode(label, "UTF-8")
                    val encodedUri = URLEncoder.encode(uri, "UTF-8")
                    val id = "intent:$encodedLabel:$encodedUri"
                    
                    val resultIntent = Intent().apply { putExtra("ELEMENT_ID", id) }
                    setResult(Activity.RESULT_OK, resultIntent)
                    finish()
                }
            }
        }
        layout.addView(btnSave)
        
        setContentView(layout)
    }
}
