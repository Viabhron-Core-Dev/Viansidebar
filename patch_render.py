with open("app/src/main/java/com/example/service/WidgetsGridPageView.kt", "r") as f:
    content = f.read()

import_manager = """import com.example.utils.AppWidgetHelper
import org.json.JSONArray"""
new_import = """import com.example.utils.AppWidgetHelper
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.json.JSONArray"""
content = content.replace(import_manager, new_import)

old_loop = """            for (item in items) {
                try {
                    val info = appWidgetManager.getAppWidgetInfo(item.id)
                    if (info != null) {
                        val hostView = host.createView(context, item.id, info)
                        
                        val wCols = minOf(item.cols, totalCols)
                        val wRows = item.rows
                        
                        val params = GridLayout.LayoutParams().apply {
                            width = cellWidth * wCols
                            height = cellHeight * wRows
                            columnSpec = GridLayout.spec(GridLayout.UNDEFINED, wCols)
                            rowSpec = GridLayout.spec(GridLayout.UNDEFINED, wRows)
                        }
                        gridLayout.addView(hostView, params)
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }"""

new_loop = """            val appsManager = SidebarAppsManager(context, prefs, CoroutineScope(Dispatchers.IO), "wg_${pageId}") {}
            appsManager.ensureLoaded()
            
            for (item in items) {
                try {
                    if (item.id.startsWith("widget:")) {
                        val wId = item.id.removePrefix("widget:").toIntOrNull() ?: continue
                        val info = appWidgetManager.getAppWidgetInfo(wId)
                        if (info != null) {
                            val hostView = host.createView(context, wId, info)
                            
                            val wCols = minOf(item.cols, totalCols)
                            val wRows = item.rows
                            
                            val params = GridLayout.LayoutParams().apply {
                                width = cellWidth * wCols
                                height = cellHeight * wRows
                                columnSpec = GridLayout.spec(GridLayout.UNDEFINED, wCols)
                                rowSpec = GridLayout.spec(GridLayout.UNDEFINED, wRows)
                            }
                            gridLayout.addView(hostView, params)
                        }
                    } else {
                        val parsed = appsManager.parseId(item.id)
                        if (parsed != null) {
                            val elementView = android.view.LayoutInflater.from(context).inflate(com.example.R.layout.item_sidebar_app, null, false)
                            val icon = elementView.findViewById<android.widget.ImageView>(com.example.R.id.app_icon)
                            val label = elementView.findViewById<android.widget.TextView>(com.example.R.id.app_label)
                            
                            label.text = parsed.label
                            
                            CoroutineScope(Dispatchers.Main).launch {
                                val bmp = appsManager.getIconBitmap(item.id)
                                if (bmp != null) {
                                    icon.setImageBitmap(bmp)
                                }
                            }
                            
                            elementView.setOnClickListener {
                                val i = Intent(context, FloatingReaderService::class.java).apply {
                                    action = "LAUNCH_APP"
                                    putExtra("APP_PACKAGE", item.id)
                                }
                                context.startService(i)
                            }
                            
                            val wCols = minOf(item.cols, totalCols)
                            val wRows = item.rows
                            
                            val params = GridLayout.LayoutParams().apply {
                                width = cellWidth * wCols
                                height = cellHeight * wRows
                                columnSpec = GridLayout.spec(GridLayout.UNDEFINED, wCols)
                                rowSpec = GridLayout.spec(GridLayout.UNDEFINED, wRows)
                            }
                            gridLayout.addView(elementView, params)
                        }
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }"""
content = content.replace(old_loop, new_loop)

with open("app/src/main/java/com/example/service/WidgetsGridPageView.kt", "w") as f:
    f.write(content)
