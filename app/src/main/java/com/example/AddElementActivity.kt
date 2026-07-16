package com.example

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.view.Gravity
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ListView
import android.widget.TextView
import androidx.activity.ComponentActivity

class AddElementActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutParams = ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
            setBackgroundColor(Color.BLACK)
            setPadding(32, 32, 32, 32)
        }
        
        val title = TextView(this).apply {
            text = "Add Element"
            setTextColor(Color.WHITE)
            textSize = 24f
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, 32)
        }
        layout.addView(title)
        
        val items = listOf(
            "App",
            "Action: eBook Reader",
            "Action: Screenshot",
            "Action: Quick Tiles",
            "Action: Compass",
            "Action: BlockAds",
            "Action: Scheduler",
            "Action: Log Keeper",
            "Action: Floating Calculator",
            "Custom Intent"
        )
        
        val list = ListView(this).apply {
            adapter = ArrayAdapter(this@AddElementActivity, android.R.layout.simple_list_item_1, items)
            setBackgroundColor(Color.parseColor("#222222"))
            setOnItemClickListener { _, _, position, _ ->
                when (position) {
                    0 -> {
                        val intent = Intent(this@AddElementActivity, AppPickerActivity::class.java)
                        startActivityForResult(intent, 200)
                    }
                    1 -> finishWithId("action:ebook_reader")
                    2 -> finishWithId("action:screenshot")
                    3 -> finishWithId("action:quick_tiles")
                    4 -> finishWithId("action:compass")
                    5 -> finishWithId("action:blockads")
                    6 -> finishWithId("action:scheduler")
                    7 -> finishWithId("action:log_keeper")
                    8 -> finishWithId("action:calculator")
                    9 -> {
                        val intent = Intent(this@AddElementActivity, IntentPickerActivity::class.java)
                        startActivityForResult(intent, 300)
                    }
                }
            }
        }
        
        // Fix text color in list view
        list.adapter = object : ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, items) {
            override fun getView(position: Int, convertView: android.view.View?, parent: ViewGroup): android.view.View {
                val view = super.getView(position, convertView, parent) as TextView
                view.setTextColor(Color.WHITE)
                return view
            }
        }
        
        layout.addView(list)
        setContentView(layout)
    }
    
    private fun finishWithId(id: String) {
        if (intent?.action == "SELECT_ELEMENT_FOR_HANDLE") {
            val prefix = intent.getStringExtra("handle_prefix") ?: return
            val gesture = intent.getStringExtra("gesture") ?: return
            val prefs = getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
            prefs.edit().putString("${prefix}$gesture", "open_element:$id").apply()
            
            // Notify service to reload configuration
            val updateIntent = Intent(this, com.example.service.FloatingReaderService::class.java).apply {
                action = "UPDATE_CONFIG"
            }
            startService(updateIntent)
        } else {
            val resultIntent = Intent().apply { putExtra("ELEMENT_ID", id) }
            setResult(Activity.RESULT_OK, resultIntent)
        }
        finish()
    }
    
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode == Activity.RESULT_OK && data != null) {
            val id = data.getStringExtra("ELEMENT_ID")
            if (id != null) {
                finishWithId(id)
            }
        }
    }
}
