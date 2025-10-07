import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
import matplotlib.pyplot as plt

# ---------------- Database Setup ----------------
conn = sqlite3.connect("participation.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS participation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    date TEXT,
    mark INTEGER
)
""")
conn.commit()

# ---------------- Functions ----------------
def add_record():
    name = entry_name.get().strip()
    try:
        mark = int(entry_mark.get())
    except ValueError:
        messagebox.showerror("Error", "Mark must be a number")
        return

    if not name or mark < 0 or mark > 10:
        messagebox.showerror("Error", "Enter valid name and mark (0-10)")
        return

    date = datetime.date.today().isoformat()
    cursor.execute("INSERT INTO participation (student_name, date, mark) VALUES (?, ?, ?)",
                   (name, date, mark))
    conn.commit()
    messagebox.showinfo("Success", f"Added {name}'s mark: {mark}")
    entry_name.delete(0, tk.END)
    entry_mark.delete(0, tk.END)

def view_report():
    cursor.execute("SELECT student_name, AVG(mark) FROM participation GROUP BY student_name")
    results = cursor.fetchall()

    report = ""
    class_marks = []

    for student, avg in results:
        avg_score = round(avg, 2)
        class_marks.append(avg_score)

        if avg_score >= 8:
            status = "Highly Engaged 🎯"
        elif avg_score >= 5:
            status = "Moderate 🙂"
        else:
            status = "Needs Attention ⚠️"

        report += f"{student}: {avg_score} → {status}\n"

    # Class average & recommendations
    if class_marks:
        class_avg = sum(class_marks) / len(class_marks)
        report += f"\nClass Average: {round(class_avg, 2)}\n"

        if class_avg < 5:
            report += "Recommendation: Use group activities & Q&A.\n"
        elif class_avg < 8:
            report += "Recommendation: Add interactive elements.\n"
        else:
            report += "Recommendation: Keep up the good work!\n"

    messagebox.showinfo("Report", report)

def show_chart():
    cursor.execute("SELECT date, AVG(mark) FROM participation GROUP BY date ORDER BY date")
    results = cursor.fetchall()

    if not results:
        messagebox.showinfo("No Data", "No records to show")
        return

    dates = [r[0] for r in results]
    avgs = [r[1] for r in results]

    plt.plot(dates, avgs, marker="o")
    plt.title("Class Concentration Trend")
    plt.xlabel("Date")
    plt.ylabel("Average Participation")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ---------------- UI Setup ----------------
root = tk.Tk()
root.title("Student Concentration Tracker")

tk.Label(root, text="Student Name:").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Participation Mark (0-10):").grid(row=1, column=0, padx=5, pady=5)
entry_mark = tk.Entry(root)
entry_mark.grid(row=1, column=1, padx=5, pady=5)

btn_add = tk.Button(root, text="Add Record", command=add_record)
btn_add.grid(row=2, column=0, columnspan=2, pady=10)

btn_report = tk.Button(root, text="View Report", command=view_report)
btn_report.grid(row=3, column=0, columnspan=2, pady=10)

btn_chart = tk.Button(root, text="Show Trend Chart", command=show_chart)
btn_chart.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
