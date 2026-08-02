package com.example.service

import android.app.AlertDialog
import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.FrameLayout
import android.widget.TextView
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.data.AppDatabase
import com.example.R
import com.example.data.SchedulerTask
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class SchedulerPageView(context: Context, private val scope: CoroutineScope) : FrameLayout(context) {
    private val db = AppDatabase.getDatabase(context)
    private val recyclerView: RecyclerView
    private val tvEmpty: TextView
    private val adapter: TaskAdapter

    init {
        com.example.LogKeeper.writeLog("Scheduler", "Opened scheduler page")
        LayoutInflater.from(context).inflate(R.layout.page_scheduler, this, true)

        recyclerView = findViewById(R.id.recycler_view)
        tvEmpty = findViewById(R.id.tv_empty)

        recyclerView.layoutManager = LinearLayoutManager(context)
        adapter = TaskAdapter { task -> showDialog(task) }
        recyclerView.adapter = adapter

        findViewById<View>(R.id.fab_add).setOnClickListener {
            showDialog(null)
        }

        loadTasks()
    }

    private fun loadTasks() {
        scope.launch(Dispatchers.Main) {
            db.schedulerTaskDao().getAllTasks().collect { tasks ->
                adapter.submitList(tasks)
                if (tasks.isEmpty()) {
                    tvEmpty.visibility = View.VISIBLE
                    recyclerView.visibility = View.GONE
                } else {
                    tvEmpty.visibility = View.GONE
                    recyclerView.visibility = View.VISIBLE
                }
            }
        }
    }

    private fun showDialog(taskToEdit: SchedulerTask?) {
        val dialogView = LayoutInflater.from(context).inflate(R.layout.dialog_scheduler_task, null)
        val tvTitle = dialogView.findViewById<TextView>(R.id.tv_dialog_title)
        val etTitle = dialogView.findViewById<EditText>(R.id.et_title)
        val etNote = dialogView.findViewById<EditText>(R.id.et_note)
        val llOffsets = dialogView.findViewById<View>(R.id.ll_offsets)
        val etDays = dialogView.findViewById<EditText>(R.id.et_days)
        val etHours = dialogView.findViewById<EditText>(R.id.et_hours)
        val btnDelete = dialogView.findViewById<Button>(R.id.btn_delete)
        val btnCancel = dialogView.findViewById<Button>(R.id.btn_cancel)
        val btnSave = dialogView.findViewById<Button>(R.id.btn_save)

        val isEditing = taskToEdit != null
        tvTitle.text = if (isEditing) "Edit Task" else "Add Task"

        if (isEditing) {
            etTitle.setText(taskToEdit!!.title)
            etNote.setText(taskToEdit.note)
            llOffsets.visibility = View.GONE
            btnDelete.visibility = View.VISIBLE
        }

        val dialog = AlertDialog.Builder(context)
            .setView(dialogView)
            .create()

        btnDelete.setOnClickListener {
            taskToEdit?.let {
                scope.launch(Dispatchers.IO) {
                    db.schedulerTaskDao().delete(it)
                }
            }
            dialog.dismiss()
        }

        btnCancel.setOnClickListener { dialog.dismiss() }

        btnSave.setOnClickListener {
            val title = etTitle.text.toString().ifEmpty { "Untitled" }
            val note = etNote.text.toString()

            val targetTime = if (isEditing) {
                taskToEdit!!.timeMillis
            } else {
                val days = etDays.text.toString().toLongOrNull() ?: 0L
                val hours = etHours.text.toString().toLongOrNull() ?: 0L
                System.currentTimeMillis() + (days * 24 * 60 * 60 * 1000) + (hours * 60 * 60 * 1000)
            }

            val task = SchedulerTask(
                id = taskToEdit?.id ?: 0,
                title = title,
                note = note,
                timeMillis = targetTime
            )

            scope.launch(Dispatchers.IO) {
                if (isEditing) {
                    db.schedulerTaskDao().update(task)
                } else {
                    db.schedulerTaskDao().insert(task)
                }
            }
            dialog.dismiss()
        }

        dialog.show()
    }

    private inner class TaskAdapter(private val onLongClick: (SchedulerTask) -> Unit) : RecyclerView.Adapter<TaskAdapter.ViewHolder>() {
        private var tasks = emptyList<SchedulerTask>()
        private val dateFormatter = SimpleDateFormat("MMM dd, yyyy HH:mm", Locale.getDefault())

        fun submitList(newTasks: List<SchedulerTask>) {
            tasks = newTasks
            notifyDataSetChanged()
        }

        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
            val view = LayoutInflater.from(parent.context).inflate(R.layout.item_scheduler_task, parent, false)
            return ViewHolder(view)
        }

        override fun onBindViewHolder(holder: ViewHolder, position: Int) {
            val task = tasks[position]
            holder.tvTitle.text = task.title
            if (task.note.isNotEmpty()) {
                holder.tvNote.visibility = View.VISIBLE
                holder.tvNote.text = task.note
            } else {
                holder.tvNote.visibility = View.GONE
            }
            holder.tvTime.text = dateFormatter.format(Date(task.timeMillis))
            
            holder.itemView.setOnLongClickListener {
                onLongClick(task)
                true
            }
        }

        override fun getItemCount() = tasks.size

        inner class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
            val tvTitle: TextView = itemView.findViewById(R.id.tv_title)
            val tvNote: TextView = itemView.findViewById(R.id.tv_note)
            val tvTime: TextView = itemView.findViewById(R.id.tv_time)
        }
    }
}
