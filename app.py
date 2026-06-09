import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
from datetime import datetime, timedelta
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
class StudyPlannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Study Planner")
        self.geometry("1100 integrity")
        self.geometry("1150x750") 
        self.tasks_list = []
        self.appointments = []
        self.days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
        self.times = ['6am','7am','8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm',
                      '5pm','6pm','7pm','8pm','9pm','10pm','11pm','12am','1am','2am','3am','4am','5am']
        
        self.schedule_df = pd.DataFrame('---', index=self.times, columns=self.days)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="STUDY PLANNER", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        self.btn_tasks = ctk.CTkButton(self.sidebar, text=" Tasks", command=lambda: self.show_frame("tasks"))
        self.btn_tasks.grid(row=1, column=0, padx=20, pady=10)

        self.btn_schedule = ctk.CTkButton(self.sidebar, text=" Weekly Schedule", command=lambda: self.show_frame("schedule"))
        self.btn_schedule.grid(row=2, column=0, padx=20, pady=10)

        self.btn_apps = ctk.CTkButton(self.sidebar, text=" Appointments", command=lambda: self.show_frame("appointments"))
        self.btn_apps.grid(row=3, column=0, padx=20, pady=10)

        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.frames = {}
        self.setup_task_frame()
        self.setup_schedule_frame()
        self.setup_appointment_frame()
        
        self.show_frame("tasks")

    def setup_task_frame(self):
        frame = ctk.CTkFrame(self.container)
        self.frames["tasks"] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(frame, text="My Daily Tasks", font=("Arial", 24)).pack(pady=10)
        input_frame = ctk.CTkFrame(frame)
        input_frame.pack(fill="x", padx=20, pady=10)
        self.task_entry = ctk.CTkEntry(input_frame, placeholder_text="Task Name ")
        self.task_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        self.days_left_var = ctk.StringVar(value="1")
        ctk.CTkLabel(input_frame, text="Days until due:").pack(side="left")
        ctk.CTkOptionMenu(input_frame, values=["1", "2", "3", "7", "14"], variable=self.days_left_var, width=70).pack(side="left", padx=5)
        ctk.CTkButton(input_frame, text="Add Task", width=100, command=self.gui_add_task).pack(side="right", padx=10)
        self.scrollable_tasks = ctk.CTkScrollableFrame(frame, label_text="To-Do List & Deadlines")
        self.scrollable_tasks.pack(fill="both", expand=True, padx=20, pady=10)

    def gui_add_task(self):
        title = self.task_entry.get()
        if title.strip():
            due_date = datetime.now() + timedelta(days=int(self.days_left_var.get()))
            task_obj = {"title": title, "completed": False, "due_date": due_date}
            self.tasks_list.append(task_obj)
            self.refresh_task_list()
            self.task_entry.delete(0, 'end')
        else:
            messagebox.showwarning("Input Error", "Please enter a task title")

    def refresh_task_list(self):
        for widget in self.scrollable_tasks.winfo_children(): widget.destroy()
        for i, task in enumerate(self.tasks_list):
            f = ctk.CTkFrame(self.scrollable_tasks)
            f.pack(fill="x", pady=5)
            remaining = task['due_date'] - datetime.now()
            days_str = f"{remaining.days}d left" if remaining.days >= 0 else "OVERDUE"
            color = "white" if remaining.days >= 0 else "#e76f51"
            label_text = f"{"" if task['completed'] else '⏳'} {task['title']} | Due: {task['due_date'].strftime('%Y-%m-%d')} ({days_str})"
            ctk.CTkLabel(f, text=label_text, text_color=color).pack(side="left", padx=10)
            ctk.CTkButton(f, text="Delete", fg_color="#ae2012", width=60, command=lambda idx=i: self.gui_delete_task(idx)).pack(side="right", padx=5)
            ctk.CTkButton(f, text="+1 Day", fg_color="#457b9d", width=60, command=lambda idx=i: self.gui_postpone_task(idx)).pack(side="right", padx=5)
            if not task["completed"]:
                ctk.CTkButton(f, text="Done", fg_color="#2b9348", width=60, command=lambda idx=i: self.gui_complete_task(idx)).pack(side="right", padx=5)

    def gui_postpone_task(self, idx):
        self.tasks_list[idx]['due_date'] += timedelta(days=1)
        self.refresh_task_list()

    def gui_complete_task(self, idx):
        self.tasks_list[idx]["completed"] = True
        self.refresh_task_list()

    def gui_delete_task(self, idx):
        del self.tasks_list[idx]
        self.refresh_task_list()

    def setup_appointment_frame(self):
        frame = ctk.CTkFrame(self.container)
        self.frames["appointments"] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(frame, text="Appointments & Exams", font=("Arial", 24)).pack(pady=10)

        input_f = ctk.CTkFrame(frame)
        input_f.pack(fill="x", padx=20, pady=10)

        self.app_title = ctk.CTkEntry(input_f, placeholder_text="Title (Exam/Dr.)")
        self.app_title.grid(row=0, column=0, padx=5, pady=5)
      
        self.app_day_var = ctk.StringVar(value="Monday")
        ctk.CTkOptionMenu(input_f, values=self.days, variable=self.app_day_var, width=110).grid(row=0, column=1, padx=5)

        self.app_time_var = ctk.StringVar(value="9am")
        ctk.CTkOptionMenu(input_f, values=self.times, variable=self.app_time_var, width=90).grid(row=0, column=2, padx=5)

        self.app_date = ctk.CTkEntry(input_f, placeholder_text="YYYY-MM-DD", width=110)
        self.app_date.insert(0, datetime.now().strftime("%Y-%m-%d")) 
        self.app_date.grid(row=0, column=3, padx=5)

        ctk.CTkButton(input_f, text="Add", width=80, command=self.gui_add_appointment).grid(row=0, column=4, padx=5)

        self.scrollable_apps = ctk.CTkScrollableFrame(frame, label_text="Scheduled Appointments")
        self.scrollable_apps.pack(fill="both", expand=True, padx=20, pady=10)

    def gui_add_appointment(self):
        title = self.app_title.get()
        date_str = self.app_date.get()
        day = self.app_day_var.get()
        time_slot = self.app_time_var.get()

        if not title.strip():
            messagebox.showwarning("Input Error", "Please enter an appointment title")
            return
        existing_task = self.schedule_df.loc[time_slot, day]
        if existing_task != "---":
            messagebox.showerror("Conflict Detected", 
                                 f"You already have '{existing_task}' scheduled on {day} at {time_slot}.\n"
                                 "Please choose another time.")
            return

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            self.appointments.append({"title": title, "date": date_obj, "time": time_slot, "day": day})
            
            self.schedule_df.loc[time_slot, day] = f" {title}"
            self.update_schedule_display()
            
            self.refresh_appointments()
            self.app_title.delete(0, 'end')
        except:
            messagebox.showerror("Format Error", "Use YYYY-MM-DD for date")

    def refresh_appointments(self):
        for widget in self.scrollable_apps.winfo_children(): widget.destroy()
        for i, app in enumerate(self.appointments):
            f = ctk.CTkFrame(self.scrollable_apps)
            f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=f" {app['title']} - {app['day']} {app['time']} ({app['date'].strftime('%b %d')})").pack(side="left", padx=10)
            ctk.CTkButton(f, text="Remove", fg_color="transparent", border_width=1, width=60, 
                             command=lambda idx=i: self.gui_del_appointment(idx)).pack(side="right", padx=5)

    def gui_del_appointment(self, idx):
        app = self.appointments[idx]
        self.schedule_df.loc[app['time'], app['day']] = "---"
        self.update_schedule_display()
        del self.appointments[idx]
        self.refresh_appointments()

    def setup_schedule_frame(self):
        frame = ctk.CTkFrame(self.container)
        self.frames["schedule"] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(frame, text="Weekly Study Schedule", font=("Arial", 24)).pack(pady=10)
        tool_bar = ctk.CTkFrame(frame)
        tool_bar.pack(fill="x", padx=20, pady=5)
        self.day_var = ctk.StringVar(value="Monday")
        ctk.CTkOptionMenu(tool_bar, values=self.days, variable=self.day_var, width=120).grid(row=0, column=0, padx=5)
        self.start_var = ctk.StringVar(value="9am")
        ctk.CTkOptionMenu(tool_bar, values=self.times, variable=self.start_var, width=100).grid(row=0, column=1, padx=5)
        self.end_var = ctk.StringVar(value="11am")
        ctk.CTkOptionMenu(tool_bar, values=self.times, variable=self.end_var, width=100).grid(row=0, column=2, padx=5)
        self.sched_act_entry = ctk.CTkEntry(tool_bar, placeholder_text="Subject")
        self.sched_act_entry.grid(row=0, column=3, padx=5)
        ctk.CTkButton(tool_bar, text="Set Time Slot", command=self.gui_update_schedule).grid(row=0, column=4, padx=5)
        self.schedule_textbox = ctk.CTkTextbox(frame, font=("Courier New", 12), wrap="none")
        self.schedule_textbox.pack(fill="both", expand=True, padx=20, pady=20)
        self.update_schedule_display()

    def gui_update_schedule(self):
        try:
            day, start, end, act = self.day_var.get(), self.start_var.get(), self.end_var.get(), self.sched_act_entry.get()
            if not act.strip():
                messagebox.showwarning("Input Error", "Please enter a subject name")
                return
                
            s_idx = self.schedule_df.index.get_loc(start)
            e_idx = self.schedule_df.index.get_loc(end)
            if s_idx >= e_idx:
                messagebox.showerror("Time Error", "End time must be strictly after start time in the list layout!")
                return
            self.schedule_df.iloc[s_idx:e_idx, self.schedule_df.columns.get_loc(day)] = act
            self.update_schedule_display()
            self.sched_act_entry.delete(0, 'end')
        except Exception as e: messagebox.showerror("Error", str(e))

    def update_schedule_display(self):
        self.schedule_textbox.delete("1.0", "end")
        with pd.option_context('display.max_columns', None, 'display.width', 1000):
            self.schedule_textbox.insert("1.0", self.schedule_df.to_string())

    def show_frame(self, page_name):
        self.frames[page_name].tkraise()

if __name__ == "__main__":
    app = StudyPlannerApp()
    app.mainloop()