# Lost property scanner
import csv
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os


# Load student data from CSV

students = {}

if not os.path.exists("students.csv"):
    messagebox.showerror("Error", "students.csv not found")
    raise SystemExit

with open("students.csv", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader, None)  # Skip header safely
    for row in reader:
        if len(row) < 5:
            continue  # Skip bad rows
        student_id = row[0].strip()
        students[student_id] = row



# scan hanling

scan_in_progress = False

def process_scan(event=None):
    global scan_in_progress
    if scan_in_progress:
        return
    scan_in_progress = True
    root.after(10, handle_scan)


def handle_scan():
    global scan_in_progress

    scanned_id = entry.get().strip()
    entry.delete(0, tk.END)
    entry.focus_force()
    scan_in_progress = False

    if not scanned_id:
        return

    if scanned_id in students:
        row = students[scanned_id]
        info.set(
            f"Name: {row[1]}\n"
            f"Class: {row[3]}\n"
            f"Teacher: {row[2]}\n"
            f"Parent Email: {row[4]}"
        )
    else:
        messagebox.showerror("Error", "Student not found")
        entry.focus_force()



# gui setup

root = tk.Tk()
root.title("Lost Property Scanner")
root.geometry("800x500")

# Load and resize logo
if os.path.exists("Copy of lost property final.png"):
    img = Image.open("Copy of lost property final.png")
    img = img.resize((150, 150))
    logo = ImageTk.PhotoImage(img)
    tk.Label(root, image=logo).pack(pady=10)
else:
    tk.Label(root, text="Lost Property", font=("Arial", 24)).pack(pady=10)

    
tk.Label(
    root,
    text="Scan Student QR Code",
    font=("Arial", 20)
).pack(pady=10)

# Entry box for scaner input
entry = tk.Entry(root, font=("Arial", 18))
entry.pack()
entry.focus_force()
entry.configure(exportselection=0)

# Bind scanner keys
entry.bind("<Return>", process_scan)
entry.bind("<KP_Enter>", process_scan)
entry.bind("<Tab>", process_scan)

# Output label
info = tk.StringVar()
tk.Label(
    root,
    textvariable=info,
    font=("Arial", 18),
    justify="left"
).pack(pady=20)

# Start app
root.mainloop()




