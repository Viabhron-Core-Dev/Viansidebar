package com.example.service

import android.content.Context
import android.graphics.PixelFormat
import android.os.Build
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.ViewConfiguration
import android.view.WindowManager
import android.widget.FrameLayout
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.VolumeUp
import android.speech.tts.TextToSpeech
import java.util.Locale
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.ComposeView
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleRegistry
import androidx.lifecycle.ViewModelStore
import androidx.lifecycle.ViewModelStoreOwner
import androidx.lifecycle.setViewTreeLifecycleOwner
import androidx.lifecycle.setViewTreeViewModelStoreOwner
import androidx.savedstate.SavedStateRegistry
import androidx.savedstate.SavedStateRegistryController
import androidx.savedstate.SavedStateRegistryOwner
import androidx.savedstate.setViewTreeSavedStateRegistryOwner
import androidx.room.Room
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlin.math.roundToInt

class DictionaryWindowManager(private val context: Context) {

    private val windowManager = context.getSystemService(Context.WINDOW_SERVICE) as WindowManager
    private val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)

    private var floatingView: View? = null
    private var foldedView: View? = null

    private var layoutParams: WindowManager.LayoutParams? = null
    private var foldedLayoutParams: WindowManager.LayoutParams? = null

    private val db = Room.databaseBuilder(context, DictionaryDatabase::class.java, "dictionary.db").fallbackToDestructiveMigration().build()
    private var isFullScreen = false
    private val isFullScreenState = androidx.compose.runtime.mutableStateOf(false)

    fun show(fullScreen: Boolean = false) {
        if (floatingView != null) {
            if (isFullScreen != fullScreen) {
                isFullScreen = fullScreen
        isFullScreenState.value = fullScreen
                if (isFullScreen) {
                    layoutParams?.width = android.view.WindowManager.LayoutParams.MATCH_PARENT
                    layoutParams?.height = android.view.WindowManager.LayoutParams.MATCH_PARENT
                    layoutParams?.x = 0
                    layoutParams?.y = 0
                } else {
                    layoutParams?.width = prefs.getInt("dict_window_width", 600)
                    layoutParams?.height = prefs.getInt("dict_window_height", 800)
                    layoutParams?.x = prefs.getInt("dict_window_x", 100)
                    layoutParams?.y = prefs.getInt("dict_window_y", 100)
                }
                windowManager.updateViewLayout(floatingView, layoutParams)
                // Note: we can't easily trigger recomposition of isFullScreen from here without a state, but this is fine for layout.
                // Wait, if it's a compose state, we might need a MutableState for isFullScreen.
            }
            return
        }
        if (foldedView != null) return
        isFullScreen = fullScreen
        isFullScreenState.value = fullScreen

        val width = prefs.getInt("dict_window_width", 600)
        val height = prefs.getInt("dict_window_height", 800)
        val x = prefs.getInt("dict_window_x", 100)
        val y = prefs.getInt("dict_window_y", 100)

        layoutParams = WindowManager.LayoutParams(
            if (isFullScreen) WindowManager.LayoutParams.MATCH_PARENT else width,
            if (isFullScreen) WindowManager.LayoutParams.MATCH_PARENT else height,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY else WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL or WindowManager.LayoutParams.FLAG_WATCH_OUTSIDE_TOUCH,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            this.x = if (isFullScreen) 0 else x
            this.y = if (isFullScreen) 0 else y
        }

        floatingView = FrameLayout(context).apply {
            addView(ComposeView(context).apply {
                setContent {
                    MaterialTheme(colorScheme = darkColorScheme()) {
                        DictionaryWindowContent(
                            onClose = { close() },
                            onFold = { fold() },
                            onDrag = { dx, dy ->
                                if (!isFullScreen) {
                                    this@DictionaryWindowManager.layoutParams?.x = (this@DictionaryWindowManager.layoutParams?.x ?: 0) + dx.roundToInt()
                                    this@DictionaryWindowManager.layoutParams?.y = (this@DictionaryWindowManager.layoutParams?.y ?: 0) + dy.roundToInt()
                                    windowManager.updateViewLayout(floatingView, this@DictionaryWindowManager.layoutParams)
                                    prefs.edit().putInt("dict_window_x", this@DictionaryWindowManager.layoutParams?.x ?: 0)
                                        .putInt("dict_window_y", this@DictionaryWindowManager.layoutParams?.y ?: 0).apply()
                                }
                            },
                            onResize = { dx, dy ->
                                if (!isFullScreen) {
                                    this@DictionaryWindowManager.layoutParams?.width = ((this@DictionaryWindowManager.layoutParams?.width ?: 0) + dx.roundToInt()).coerceAtLeast(300)
                                    this@DictionaryWindowManager.layoutParams?.height = ((this@DictionaryWindowManager.layoutParams?.height ?: 0) + dy.roundToInt()).coerceAtLeast(400)
                                    windowManager.updateViewLayout(floatingView, this@DictionaryWindowManager.layoutParams)
                                    prefs.edit().putInt("dict_window_width", this@DictionaryWindowManager.layoutParams?.width ?: 0)
                                        .putInt("dict_window_height", this@DictionaryWindowManager.layoutParams?.height ?: 0).apply()
                                }
                            },
                            onToggleFullscreen = {
                                isFullScreen = !isFullScreen
                                isFullScreenState.value = isFullScreen
                                if (isFullScreen) {
                                    this@DictionaryWindowManager.layoutParams?.width = WindowManager.LayoutParams.MATCH_PARENT
                                    this@DictionaryWindowManager.layoutParams?.height = WindowManager.LayoutParams.MATCH_PARENT
                                    this@DictionaryWindowManager.layoutParams?.x = 0
                                    this@DictionaryWindowManager.layoutParams?.y = 0
                                } else {
                                    this@DictionaryWindowManager.layoutParams?.width = prefs.getInt("dict_window_width", 600)
                                    this@DictionaryWindowManager.layoutParams?.height = prefs.getInt("dict_window_height", 800)
                                    this@DictionaryWindowManager.layoutParams?.x = prefs.getInt("dict_window_x", 100)
                                    this@DictionaryWindowManager.layoutParams?.y = prefs.getInt("dict_window_y", 100)
                                }
                                windowManager.updateViewLayout(floatingView, this@DictionaryWindowManager.layoutParams)
                            },
                            isFullScreen = isFullScreenState.value
                        )
                    }
                }
            })
        }
        
        setupLifecycle(floatingView!!)
        windowManager.addView(floatingView, this@DictionaryWindowManager.layoutParams)
    }

    private fun fold() {
        if (floatingView != null) {
            windowManager.removeView(floatingView)
            floatingView = null
        }

        val x = prefs.getInt("dict_folded_x", 100)
        val y = prefs.getInt("dict_folded_y", 100)

        foldedLayoutParams = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY else WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            this.x = x
            this.y = y
        }

        foldedView = FrameLayout(context).apply {
            addView(ComposeView(context).apply {
                setContent {
                    MaterialTheme(colorScheme = darkColorScheme()) {
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .clip(CircleShape)
                                .background(Color(0xFF6200EA))
                                .pointerInput(Unit) {
                                    detectDragGestures(
                                        onDrag = { change, dragAmount ->
                                            change.consume()
                                            foldedLayoutParams?.x = (foldedLayoutParams?.x ?: 0) + dragAmount.x.roundToInt()
                                            foldedLayoutParams?.y = (foldedLayoutParams?.y ?: 0) + dragAmount.y.roundToInt()
                                            windowManager.updateViewLayout(foldedView, foldedLayoutParams)
                                        },
                                        onDragEnd = {
                                            prefs.edit().putInt("dict_folded_x", foldedLayoutParams?.x ?: 0)
                                                .putInt("dict_folded_y", foldedLayoutParams?.y ?: 0).apply()
                                        }
                                    )
                                }
                                .clickable {
                                    unfold()
                                },
                            contentAlignment = Alignment.Center
                        ) {
                            Text("D", color = Color.White, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            })
        }
        
        setupLifecycle(foldedView!!)
        windowManager.addView(foldedView, foldedLayoutParams)
    }

    private fun unfold() {
        if (foldedView != null) {
            windowManager.removeView(foldedView)
            foldedView = null
        }
        show()
    }

    private fun close() {
        if (floatingView != null) {
            windowManager.removeView(floatingView)
            floatingView = null
        }
        if (foldedView != null) {
            windowManager.removeView(foldedView)
            foldedView = null
        }
    }

    @OptIn(ExperimentalMaterial3Api::class)
    @Composable
    private fun DictionaryWindowContent(
        onClose: () -> Unit,
        onFold: () -> Unit,
        onDrag: (Float, Float) -> Unit,
        onResize: (Float, Float) -> Unit,
        onToggleFullscreen: () -> Unit,
        isFullScreen: Boolean
    ) {
        val tts = remember {
            var ttsInstance: TextToSpeech? = null
            ttsInstance = TextToSpeech(context) { status ->
                if (status == TextToSpeech.SUCCESS) {
                    ttsInstance?.language = Locale.US
                }
            }
            ttsInstance
        }

        DisposableEffect(Unit) {
            onDispose {
                tts?.stop()
                tts?.shutdown()
            }
        }

        var searchQuery by remember { mutableStateOf("") }
        var searchResults by remember { mutableStateOf<List<DictionaryEntry>>(emptyList()) }
        var selectedEntry by remember { mutableStateOf<DictionaryEntry?>(null) }
        var history by remember { mutableStateOf<List<String>>(prefs.getString("dict_history", "")?.split(",")?.filter { it.isNotBlank() } ?: emptyList()) }

        LaunchedEffect(searchQuery) {
            if (searchQuery.isNotBlank()) {
                withContext(Dispatchers.IO) {
                    searchResults = db.dictionaryDao().searchWords("$searchQuery%", context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE).getString("active_dict", "English") ?: "English")
                }
            } else {
                searchResults = emptyList()
            }
        }

        Surface(
            modifier = Modifier.fillMaxSize().clip(if (isFullScreen) RoundedCornerShape(0.dp) else RoundedCornerShape(12.dp)),
            color = Color(0xFF1E1E2C)
        ) {
            Column(modifier = Modifier.fillMaxSize()) {
                // Top Bar (Draggable)
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(Color(0xFF2A2A3C))
                        .pointerInput(Unit) {
                            detectTapGestures(
                                onDoubleTap = { onToggleFullscreen() }
                            )
                        }
                        .pointerInput(Unit) {
                            detectDragGestures { change, dragAmount ->
                                change.consume()
                                onDrag(dragAmount.x, dragAmount.y)
                            }
                        }
                        .padding(8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Dictionary", color = Color.White, modifier = Modifier.weight(1f), fontWeight = FontWeight.Bold)
                    IconButton(onClick = onFold, modifier = Modifier.size(24.dp)) {
                        Icon(Icons.Default.Menu, contentDescription = "Fold", tint = Color.White)
                    }
                    Spacer(modifier = Modifier.width(8.dp))
                    IconButton(onClick = onClose, modifier = Modifier.size(24.dp)) {
                        Icon(Icons.Default.Close, contentDescription = "Close", tint = Color.White)
                    }
                }

                if (selectedEntry == null) {
                    OutlinedTextField(
                        value = searchQuery,
                        onValueChange = { searchQuery = it },
                        placeholder = { Text("Search...") },
                        modifier = Modifier.fillMaxWidth().padding(8.dp),
                        textStyle = LocalTextStyle.current.copy(color = Color.White)
                    )

                    if (searchQuery.isBlank()) {
                        Text("History", color = Color.Gray, modifier = Modifier.padding(horizontal = 8.dp))
                        LazyColumn {
                            items(history) { word ->
                                Text(
                                    text = word,
                                    color = Color.LightGray,
                                    modifier = Modifier.fillMaxWidth().clickable {
                                        searchQuery = word
                                    }.padding(8.dp)
                                )
                            }
                        }
                    } else {
                        LazyColumn(modifier = Modifier.weight(1f)) {
                            items(searchResults) { entry ->
                                Text(
                                    text = entry.word,
                                    color = Color.White,
                                    modifier = Modifier.fillMaxWidth().clickable {
                                        selectedEntry = entry
                                        val newHistory = (listOf(entry.word) + history).distinct().take(20)
                                        history = newHistory
                                        prefs.edit().putString("dict_history", newHistory.joinToString(",")).apply()
                                    }.padding(8.dp)
                                )
                            }
                        }
                    }
                } else {
                    Button(onClick = { selectedEntry = null }, modifier = Modifier.padding(8.dp)) {
                        Text("Back")
                    }
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(horizontal = 8.dp)) {
                        Text(
                            text = selectedEntry!!.word,
                            fontSize = 20.sp,
                            color = Color.White,
                            modifier = Modifier.weight(1f)
                        )
                        IconButton(onClick = {
                            tts?.speak(selectedEntry!!.word, TextToSpeech.QUEUE_FLUSH, null, null)
                        }) {
                            Icon(Icons.Default.VolumeUp, contentDescription = "Speak Word", tint = Color.White)
                        }
                    }
                    rememberScrollState().let { scrollState ->
                        Box(modifier = Modifier.weight(1f).padding(8.dp)) {
                            Text(
                                text = selectedEntry!!.definition,
                                color = Color.LightGray,
                                modifier = Modifier.fillMaxSize().verticalScroll(scrollState)
                            )
                            FloatingActionButton(
                                onClick = {
                                    tts?.speak(selectedEntry!!.definition, TextToSpeech.QUEUE_FLUSH, null, null)
                                },
                                modifier = Modifier.align(Alignment.BottomEnd).padding(16.dp),
                                containerColor = MaterialTheme.colorScheme.primary
                            ) {
                                Icon(Icons.Default.VolumeUp, contentDescription = "Speak Definition", tint = Color.White)
                            }
                        }
                    }
                }

                // Resize handle
                if (!isFullScreen) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(20.dp)
                            .background(Color(0xFF2A2A3C))
                            .pointerInput(Unit) {
                                detectDragGestures { change, dragAmount ->
                                    change.consume()
                                    onResize(dragAmount.x, dragAmount.y)
                                }
                            }
                    ) {
                        Text("///", color = Color.Gray, modifier = Modifier.align(Alignment.CenterEnd).padding(end = 8.dp))
                    }
                }
            }
        }
    }

    private fun setupLifecycle(view: View) {
        val lifecycleOwner = CustomLifecycleOwner()
        lifecycleOwner.performRestore(null)
        lifecycleOwner.handleLifecycleEvent(Lifecycle.Event.ON_CREATE)
        view.setViewTreeLifecycleOwner(lifecycleOwner)
        view.setViewTreeSavedStateRegistryOwner(lifecycleOwner)
        view.setViewTreeViewModelStoreOwner(lifecycleOwner)
        lifecycleOwner.handleLifecycleEvent(Lifecycle.Event.ON_START)
        lifecycleOwner.handleLifecycleEvent(Lifecycle.Event.ON_RESUME)
    }

    class CustomLifecycleOwner : SavedStateRegistryOwner, ViewModelStoreOwner {
        private val lifecycleRegistry = LifecycleRegistry(this)
        private val savedStateRegistryController = SavedStateRegistryController.create(this)
        private val store = ViewModelStore()

        override val lifecycle: Lifecycle get() = lifecycleRegistry
        override val savedStateRegistry: SavedStateRegistry get() = savedStateRegistryController.savedStateRegistry
        override val viewModelStore: ViewModelStore get() = store

        fun handleLifecycleEvent(event: Lifecycle.Event) {
            lifecycleRegistry.handleLifecycleEvent(event)
        }

        fun performRestore(savedState: android.os.Bundle?) {
            savedStateRegistryController.performRestore(savedState)
        }
    }
}
