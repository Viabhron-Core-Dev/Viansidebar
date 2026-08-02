package com.example.service

import android.annotation.SuppressLint
import android.content.Context
import android.graphics.PixelFormat
import android.os.Build
import android.speech.tts.TextToSpeech
import android.view.Gravity
import android.view.LayoutInflater
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
import android.view.WindowManager
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import androidx.core.widget.addTextChangedListener
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.R
import com.example.data.AppDatabase
import com.example.service.DictionaryEntry
import com.example.service.DictionaryDatabase
import com.example.service.DictionaryDao
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.util.Locale
import kotlin.math.roundToInt

class DictionaryWindowManager(private val context: Context) {
    private val windowManager = context.getSystemService(Context.WINDOW_SERVICE) as WindowManager
    private val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
    private val db = androidx.room.Room.databaseBuilder(context.applicationContext, DictionaryDatabase::class.java, "dictionary.db").fallbackToDestructiveMigration().build()

    private var floatingView: View? = null
    private var layoutParams: WindowManager.LayoutParams? = null

    private var isFullScreen = false
    private var preFullScreenWidth = 800
    private var preFullScreenHeight = 1000
    private var preFullScreenX = 100
    private var preFullScreenY = 100
    
    private var isFolded = false

    private var tts: TextToSpeech? = null
    
    private val scope = CoroutineScope(Dispatchers.Main)

    private fun initTTS() {
        if (tts == null) {
            tts = TextToSpeech(context) { status ->
                if (status == TextToSpeech.SUCCESS) {
                    tts?.language = Locale.US
                }
            }
        }
    }

    private fun toggleFullScreen(windowContainer: View, topDragBar: View) {
        if (!isFullScreen) {
            preFullScreenWidth = layoutParams?.width ?: 800
            preFullScreenHeight = layoutParams?.height ?: 1000
            preFullScreenX = layoutParams?.x ?: 100
            preFullScreenY = layoutParams?.y ?: 100
            
            val metrics = context.resources.displayMetrics
            layoutParams?.width = metrics.widthPixels
            layoutParams?.height = metrics.heightPixels
            layoutParams?.x = 0
            layoutParams?.y = 0
            isFullScreen = true
            windowContainer.background = null
        } else {
            layoutParams?.width = preFullScreenWidth
            layoutParams?.height = preFullScreenHeight
            layoutParams?.x = preFullScreenX
            layoutParams?.y = preFullScreenY
            isFullScreen = false
            windowContainer.setBackgroundResource(R.drawable.bg_floating_window)
        }
        windowManager.updateViewLayout(floatingView, layoutParams)
    }

    @SuppressLint("ClickableViewAccessibility")
    fun show(startFullscreen: Boolean = false) {
        if (floatingView != null) return

        initTTS()

        val width = prefs.getInt("dict_width", 800)
        val height = prefs.getInt("dict_height", 1000)
        val x = prefs.getInt("dict_x", 100)
        val y = prefs.getInt("dict_y", 100)

        layoutParams = WindowManager.LayoutParams(
            width,
            height,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY else WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL or WindowManager.LayoutParams.FLAG_WATCH_OUTSIDE_TOUCH,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            this.x = x
            this.y = y
        }

        floatingView = LayoutInflater.from(context).inflate(R.layout.layout_dictionary, null)
        
        val bubbleIcon = floatingView!!.findViewById<ImageView>(R.id.bubble_icon)
        val windowContainer = floatingView!!.findViewById<LinearLayout>(R.id.window_container)
        val topDragBar = floatingView!!.findViewById<LinearLayout>(R.id.top_drag_bar)
        
        val btnClose = floatingView!!.findViewById<ImageView>(R.id.btn_exit_bottom)
        val btnMinimize = floatingView!!.findViewById<ImageView>(R.id.btn_minimize_bottom)
        val btnResize = floatingView!!.findViewById<ImageView>(R.id.resize_handle)

        val searchLayout = floatingView!!.findViewById<LinearLayout>(R.id.search_layout)
        val detailLayout = floatingView!!.findViewById<LinearLayout>(R.id.detail_layout)
        
        val etSearch = floatingView!!.findViewById<EditText>(R.id.et_search)
        val tvHistoryLabel = floatingView!!.findViewById<TextView>(R.id.tv_history_label)
        val rvResults = floatingView!!.findViewById<RecyclerView>(R.id.rv_results)
        
        val btnBack = floatingView!!.findViewById<Button>(R.id.btn_back)
        val tvWord = floatingView!!.findViewById<TextView>(R.id.tv_word)
        val tvDefinition = floatingView!!.findViewById<TextView>(R.id.tv_definition)
        val btnSpeakWord = floatingView!!.findViewById<ImageView>(R.id.btn_speak_word)
        val btnSpeakDef = floatingView!!.findViewById<View>(R.id.btn_speak_def)

        var selectedEntry: DictionaryEntry? = null
        var history = prefs.getString("dict_history", "")?.split(",")?.filter { it.isNotBlank() } ?: emptyList()
        var searchResults = emptyList<DictionaryEntry>()

        rvResults.layoutManager = LinearLayoutManager(context)
        val adapter = DictionaryAdapter { word, entry ->
            if (entry != null) {
                selectedEntry = entry
            } else {
                // Clicked history item
                etSearch.setText(word)
                return@DictionaryAdapter
            }
            
            val newHistory = (listOf(word) + history).distinct().take(20)
            history = newHistory
            prefs.edit().putString("dict_history", newHistory.joinToString(",")).apply()
            
            searchLayout.visibility = View.GONE
            detailLayout.visibility = View.VISIBLE
            tvWord.text = entry.word
            tvDefinition.text = entry.definition
        }
        rvResults.adapter = adapter
        adapter.submitList(history.map { it to null })

        etSearch.addTextChangedListener { text ->
            val query = text.toString()
            if (query.isNotBlank()) {
                tvHistoryLabel.visibility = View.GONE
                scope.launch {
                    val activeDict = prefs.getString("active_dict", "English") ?: "English"
                    val results = withContext(Dispatchers.IO) {
                        db.dictionaryDao().searchWords("$query%", activeDict)
                    }
                    adapter.submitList(results.map { it.word to it })
                }
            } else {
                tvHistoryLabel.visibility = View.VISIBLE
                adapter.submitList(history.map { it to null })
            }
        }

        btnBack.setOnClickListener {
            selectedEntry = null
            searchLayout.visibility = View.VISIBLE
            detailLayout.visibility = View.GONE
        }

        btnSpeakWord.setOnClickListener {
            selectedEntry?.let { tts?.speak(it.word, TextToSpeech.QUEUE_FLUSH, null, null) }
        }

        btnSpeakDef.setOnClickListener {
            selectedEntry?.let { tts?.speak(it.definition, TextToSpeech.QUEUE_FLUSH, null, null) }
        }

        // --- Dragging Window ---
        var initialX = 0
        var initialY = 0
        var initialTouchX = 0f
        var initialTouchY = 0f
        var lastTouchTime = 0L

        topDragBar.setOnTouchListener { _, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    initialX = layoutParams!!.x
                    initialY = layoutParams!!.y
                    initialTouchX = event.rawX
                    initialTouchY = event.rawY
                    
                    val clickTime = System.currentTimeMillis()
                    if (clickTime - lastTouchTime < 300) {
                        toggleFullScreen(windowContainer, topDragBar)
                    }
                    lastTouchTime = clickTime
                    true
                }
                MotionEvent.ACTION_MOVE -> {
                    if (!isFullScreen) {
                        layoutParams!!.x = initialX + (event.rawX - initialTouchX).roundToInt()
                        layoutParams!!.y = initialY + (event.rawY - initialTouchY).roundToInt()
                        windowManager.updateViewLayout(floatingView, layoutParams)
                    }
                    true
                }
                MotionEvent.ACTION_UP -> {
                    if (!isFullScreen) {
                        prefs.edit()
                            .putInt("dict_x", layoutParams!!.x)
                            .putInt("dict_y", layoutParams!!.y)
                            .apply()
                    }
                    true
                }
                else -> false
            }
        }

        // --- Resizing ---
        btnResize.setOnTouchListener { _, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    initialX = layoutParams!!.width
                    initialY = layoutParams!!.height
                    initialTouchX = event.rawX
                    initialTouchY = event.rawY
                    true
                }
                MotionEvent.ACTION_MOVE -> {
                    if (!isFullScreen) {
                        layoutParams!!.width = Math.max(300, initialX + (event.rawX - initialTouchX).roundToInt())
                        layoutParams!!.height = Math.max(300, initialY + (event.rawY - initialTouchY).roundToInt())
                        windowManager.updateViewLayout(floatingView, layoutParams)
                    }
                    true
                }
                MotionEvent.ACTION_UP -> {
                    if (!isFullScreen) {
                        prefs.edit()
                            .putInt("dict_width", layoutParams!!.width)
                            .putInt("dict_height", layoutParams!!.height)
                            .apply()
                    }
                    true
                }
                else -> false
            }
        }
        
        // --- Dragging Bubble ---
        bubbleIcon.setOnTouchListener { _, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    initialX = layoutParams!!.x
                    initialY = layoutParams!!.y
                    initialTouchX = event.rawX
                    initialTouchY = event.rawY
                    
                    val clickTime = System.currentTimeMillis()
                    if (clickTime - lastTouchTime < 300) {
                        unfold()
                    }
                    lastTouchTime = clickTime
                    true
                }
                MotionEvent.ACTION_MOVE -> {
                    layoutParams!!.x = initialX + (event.rawX - initialTouchX).roundToInt()
                    layoutParams!!.y = initialY + (event.rawY - initialTouchY).roundToInt()
                    windowManager.updateViewLayout(floatingView, layoutParams)
                    true
                }
                MotionEvent.ACTION_UP -> {
                    val dx = Math.abs(event.rawX - initialTouchX)
                    val dy = Math.abs(event.rawY - initialTouchY)
                    if (dx < 10 && dy < 10) {
                        unfold()
                    } else {
                        prefs.edit()
                            .putInt("dict_x", layoutParams!!.x)
                            .putInt("dict_y", layoutParams!!.y)
                            .apply()
                    }
                    true
                }
                else -> false
            }
        }

        btnClose.setOnClickListener { close() }
        btnMinimize.setOnClickListener { fold() }

        windowManager.addView(floatingView, layoutParams)

        if (isFolded) {
            fold()
        } else {
            unfold()
        }
    }

    fun fold() {
        isFolded = true
        if (floatingView != null) {
            val bubbleIcon = floatingView!!.findViewById<ImageView>(R.id.bubble_icon)
            val windowContainer = floatingView!!.findViewById<LinearLayout>(R.id.window_container)
            
            windowContainer.visibility = View.GONE
            bubbleIcon.visibility = View.VISIBLE
            
            layoutParams?.width = WindowManager.LayoutParams.WRAP_CONTENT
            layoutParams?.height = WindowManager.LayoutParams.WRAP_CONTENT
            layoutParams?.flags = WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL or WindowManager.LayoutParams.FLAG_WATCH_OUTSIDE_TOUCH
            windowManager.updateViewLayout(floatingView, layoutParams)
        }
    }

    private fun unfold() {
        isFolded = false
        if (floatingView != null) {
            val bubbleIcon = floatingView!!.findViewById<ImageView>(R.id.bubble_icon)
            val windowContainer = floatingView!!.findViewById<LinearLayout>(R.id.window_container)
            
            bubbleIcon.visibility = View.GONE
            windowContainer.visibility = View.VISIBLE
            
            if (isFullScreen) {
                val metrics = context.resources.displayMetrics
                layoutParams?.width = metrics.widthPixels
                layoutParams?.height = metrics.heightPixels
                layoutParams?.x = 0
                layoutParams?.y = 0
            } else {
                layoutParams?.width = prefs.getInt("dict_width", 800)
                layoutParams?.height = prefs.getInt("dict_height", 1000)
            }
            layoutParams?.flags = WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL or WindowManager.LayoutParams.FLAG_WATCH_OUTSIDE_TOUCH
            windowManager.updateViewLayout(floatingView, layoutParams)
        }
    }

    fun close() {
        if (floatingView != null) {
            windowManager.removeView(floatingView)
            floatingView = null
        }
        tts?.stop()
        tts?.shutdown()
        tts = null
    }

    private class DictionaryAdapter(private val onItemClick: (String, DictionaryEntry?) -> Unit) : 
        RecyclerView.Adapter<DictionaryAdapter.ViewHolder>() {
        
        private var items = emptyList<Pair<String, DictionaryEntry?>>()

        fun submitList(newItems: List<Pair<String, DictionaryEntry?>>) {
            items = newItems
            notifyDataSetChanged()
        }

        class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
            val textView: TextView = view.findViewById(R.id.tv_item_text)
        }

        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
            val view = LayoutInflater.from(parent.context).inflate(R.layout.layout_dictionary_item, parent, false)
            return ViewHolder(view)
        }

        override fun onBindViewHolder(holder: ViewHolder, position: Int) {
            val item = items[position]
            holder.textView.text = item.first
            if (item.second == null) {
                holder.textView.setTextColor(android.graphics.Color.LTGRAY)
            } else {
                holder.textView.setTextColor(android.graphics.Color.WHITE)
            }
            holder.itemView.setOnClickListener { onItemClick(item.first, item.second) }
        }

        override fun getItemCount() = items.size
    }
}
