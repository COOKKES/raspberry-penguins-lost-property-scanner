import sys
import os
import csv
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in26



#  PATHS

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
PIC_DIR = os.path.join(BASE_DIR, "pic")

LOGO_PATH = "/home/kejs/Desktop/Lost property scanner final/lost_property_project/Copy of lost property final.png"
CSV_PATH = os.path.join(BASE_DIR, "students.csv")


#  LOAD STUDENT CSV

students = {}

if not os.path.exists(CSV_PATH):
    print("ERROR: students.csv not found")
    sys.exit(1)

with open(CSV_PATH, newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader, None)  # skip header
    for row in reader:
        if len(row) < 5:
            continue
        student_id = row[0].strip()
        students[student_id] = row


#  E‑INK DISPLAY CLASS

class EInkDisplay:
    def __init__(self):
        self.epd = epd4in26.EPD()
        self.epd.init()
        self.epd.Clear()

        self.base_title_size = 48
        self.base_body_size = 36

        if os.path.exists(LOGO_PATH):
            self.logo = Image.open(LOGO_PATH).convert("RGB")
        else:
            self.logo = None

    def show_student(self, name, class_name, teacher, email):
        W = self.epd.width
        H = self.epd.height

        image = Image.new("1", (W, H), 255)
        draw = ImageDraw.Draw(image)

 
        # LEFT HALF (LOGO)
        left_w = W // 2
        right_x = left_w + 20

        if self.logo:
            logo = self.logo
            aspect = logo.width / logo.height

            new_h = H
            new_w = int(new_h * aspect)

            if new_w > left_w:
                new_w = left_w
                new_h = int(new_w / aspect)

            logo_resized = logo.resize((new_w, new_h)).convert("1")
            x = (left_w - new_w) // 2
            y = (H - new_h) // 2
            image.paste(logo_resized, (x, y))


        # RIGHT SIDE TEXT CONTENT

        lines = [
            ("title", "Raspberry Penguins"),
            ("title", "Lost Property"),
            ("body", f"Name: {name}"),
            ("email",""),
            ("body", f"Class: {class_name}"),
            ("email",""),
            ("body", f"Teacher: {teacher}"),
            ("email",""),
            ("body", "Parent Email:"),
            ("email", email)
        ]

        title_size = 42
        body_size = 36
        email_size = 30

        def load_font(size):
            return ImageFont.truetype(os.path.join(PIC_DIR, "Font.ttc"), size)

        title_font = load_font(title_size)
        body_font = load_font(body_size)
        email_font = load_font(email_size)


        # SHRINK EMAIL TO FIT WIDTH

        max_width = W - right_x - 10

        while email_font.getbbox(email)[2] > max_width and email_size > 10:
            email_size -= 2
            email_font = load_font(email_size)


        # AUTO‑SHRINK VERTICAL HEIGHT

        def total_height(tf, bf, ef):
            h = 0
            for style, text in lines:
                if style == "title":
                    font = tf
                elif style == "email":
                    font = ef
                else:
                    font = bf
                bbox = font.getbbox(text if text else " ")
                h += (bbox[3] - bbox[1]) + 15
            return h

        while total_height(title_font, body_font, email_font) > H - 20 and body_size > 10:
            title_size -= 2
            body_size -= 2
            title_font = load_font(title_size)
            body_font = load_font(body_size)
            

    
    


        # DRAW TEXT

        y = 10

        for style, text in lines:
            if style == "title":
                font = title_font
            elif style == "email":
                font = email_font
            else:
                font = body_font

            draw.text((right_x, y), text, font=font, fill=0)
            bbox = font.getbbox(text if text else " ")
            y += (bbox[3] - bbox[1]) + 15


        # UPDATE DISPLAY
 
        self.epd.display(self.epd.getbuffer(image))

    def clear(self):
        self.epd.init()
        self.epd.Clear()

    def sleep(self):
        self.epd.sleep()


#  MAIN LOOP (CONSOLE INPUT)


def main():
    eink = EInkDisplay()


    print("Lost Property Scanner (Console Version)")
    print("--------------------------------------")
    print("Scan a QR code or type a student ID.")
    print("Press CTRL+C to exit.\n")
    
    


    try:
        while True:
            scanned_id = input("Scan ID: ").strip()

            if scanned_id in students:
                row = students[scanned_id]
                name = row[1]
                teacher = row[2]
                class_name = row[3]
                email = row[4]

                print("\n--- STUDENT FOUND ---")
                print(f"Name: {name}")
                print(f"Class: {class_name}")
                print(f"Teacher: {teacher}")
                print(f"Parent Email: {email}")
                print("----------------------\n")

                try:
                    eink.show_student(name, class_name, teacher, email)
                except Exception as e:
                    print("E‑ink error:", e)

            else:
                print("ERROR: Student not found.\n")
                
         


    finally:
        eink.clear()
        eink.sleep()

if __name__ == "__main__":
    main()

                
                
