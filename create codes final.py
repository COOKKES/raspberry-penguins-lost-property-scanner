# Generate student QR codes

import csv
import qrcode
import os

# Folder to store QR codes
output_folder = "qr_codes"
os.makedirs(output_folder, exist_ok=True)

# Open the CSV file containing students
with open("students.csv", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader, None)  # Skip header safely

    # Go through each student and create a QR code
    for row in reader:
        if not row or len(row) < 1:
            continue  # Skip empty/bad rows

        student_id = row[0].strip()  # Column 0 = student ID

        if not student_id:
            continue

        img = qrcode.make(student_id)
        img.save(os.path.join(output_folder, f"{student_id}.png"))

# Confirmation message
print("All student QR codes have been created!")
