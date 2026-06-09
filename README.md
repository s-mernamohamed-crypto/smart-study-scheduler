#  Modern CustomTkinter Study Planner 

A sleek, desktop-based **Study Planner & Task Management Application** designed with a modern dark interface using Python's **CustomTkinter** and **Pandas** library. 

This application offers students and professionals a streamlined system to organize weekly study goals, track project deadlines, and log physical appointments or exam times with zero calendar conflicts.

---

##  Key Features

* ** Modern Sidebar Navigation:** Quickly switch between Daily Tasks, Weekly Schedules, and Appointments.
* ** Intelligent Task Tracker:** * Add tasks and select dynamic due timelines.
    * Real-time deadline monitoring showing dynamic countdown labels (e.g., `2d left`) or automatic `OVERDUE` warnings.
    * Quick interaction buttons to extend deadlines (+1 Day), complete tasks, or delete them.
* ** Core Schedule Matrix:** * Powered by a backend **Pandas DataFrame** configured to mirror a complete multi-hour weekly matrix.
    * Bulk time-slot allocator allowing users to reserve hours for specific study subjects.
* ** Conflict Prevention System:** * When scheduling exams or group sessions, the app automatically runs validations against the schedule matrix to prevent multi-booking overlaps.

---

##  Tech Stack

* **GUI Framework:** CustomTkinter (Dark Theme & Responsive Grid Layout)
* **Core Logic & Engine:** Pandas (Dataframe parsing & mapping)
* **Backend Utilities:** Tkinter (Messagebox confirmations), Datetime (Dynamic calculations)

---

##  Installation & Setup

Get your study planner up and running using these commands:

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_USERNAME/customtkinter-study-planner.git](https://github.com/YOUR_USERNAME/customtkinter-study-planner.git)
cd customtkinter-study-planner
