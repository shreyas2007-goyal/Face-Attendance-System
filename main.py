from tkinter import *
import time

from register_student import RegisterStudent
from face_registration import FaceRecognition
from attendance import AttendanceSystem
from database import DatabaseManager


class FaceAttendanceSystem:

    def __init__(self, root):

        self.root = root
        self.root.title("AI Powered Face Attendance System")
        self.root.state("zoomed")

        self.db = DatabaseManager()

        # COLORS

        self.dark_mode = True

        self.dark_bg = "#0f172a"
        self.dark_card = "#1e293b"
        self.dark_sidebar = "#111827"

        self.light_bg = "#f1f5f9"
        self.light_card = "#ffffff"
        self.light_sidebar = "#dbeafe"

        self.bg_color = self.dark_bg
        self.card_color = self.dark_card
        self.sidebar_color = self.dark_sidebar
        self.text_color = "white"

        self.root.configure(bg=self.bg_color)

        # TOP BAR

        self.top_frame = Frame(
            self.root,
            bg=self.sidebar_color,
            height=70
        )

        self.top_frame.pack(fill=X)

        self.title_lbl = Label(
            self.top_frame,
            text=" FACE ATTENDANCE SYSTEM",
            font=("Arial", 24, "bold"),
            bg=self.sidebar_color,
            fg="white"
        )

        self.title_lbl.place(x=20, y=15)

        self.clock_lbl = Label(
            self.top_frame,
            font=("Arial", 14, "bold"),
            bg=self.sidebar_color,
            fg="#38bdf8"
        )

        self.clock_lbl.place(x=1100, y=20)

        self.update_clock()

        self.theme_btn = Button(
            self.top_frame,
            text="☀ Light Mode",
            bg="#f59e0b",
            fg="white",
            command=self.toggle_theme
        )

        self.theme_btn.place(
            x=1320,
            y=15,
            width=150,
            height=40
        )

        # SIDEBAR

        self.sidebar = Frame(
            self.root,
            bg=self.sidebar_color,
            width=250
        )

        self.sidebar.pack(
            side=LEFT,
            fill=Y
        )

        Label(
            self.sidebar,
            text="🤖 HELP SATHI",
            font=("Arial", 20, "bold"),
            bg=self.sidebar_color,
            fg="#38bdf8"
        ).pack(pady=30)

        self.create_sidebar_button(
            "👤 Register Student",
            self.open_register_student
        )

        self.create_sidebar_button(
            "🎥 Face Recognition",
            self.open_face_recognition
        )

        self.create_sidebar_button(
            "📊 Attendance",
            self.open_attendance
        )

        self.create_sidebar_button(
            "❌ Exit",
            self.exit_app
        )

        # DASHBOARD

        self.dashboard = Frame(
            self.root,
            bg=self.bg_color
        )

        self.dashboard.pack(
            fill=BOTH,
            expand=True
        )

        self.welcome_lbl = Label(
            self.dashboard,
            text="Welcome To AI Dashboard",
            font=("Arial", 30, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )

        self.welcome_lbl.place(
            x=60,
            y=30
        )

        self.subtitle_lbl = Label(
            self.dashboard,
            text="DeepFace + SQLite + OpenCV + AI",
            font=("Arial", 16),
            bg=self.bg_color,
            fg="#94a3b8"
        )

        self.subtitle_lbl.place(
            x=65,
            y=85
        )

        # CARDS

        self.total_students_lbl = self.create_card(
            60, 160,
            "👥 Total Students",
            "0",
            "#3b82f6"
        )

        self.present_students_lbl = self.create_card(
            390, 160,
            "✅ Present Today",
            "0",
            "#10b981"
        )

        self.absent_students_lbl = self.create_card(
            720, 160,
            "❌ Absent Today",
            "0",
            "#ef4444"
        )

        self.late_students_lbl = self.create_card(
            1050, 160,
            "⏰ Late Today",
            "0",
            "#f59e0b"
        )

        # FEATURES

        feature_frame = Frame(
            self.dashboard,
            bg=self.card_color
        )

        feature_frame.place(
            x=60,
            y=380,
            width=1000,
            height=250
        )

        Label(
            feature_frame,
            text="SYSTEM FEATURES",
            font=("Arial", 22, "bold"),
            bg=self.card_color,
            fg="#38bdf8"
        ).pack(pady=15)

        Label(
            feature_frame,
            text="""
• DeepFace Recognition
• Real-Time Attendance
• SQLite Database
• CSV Export
• OpenCV Camera
• Student Analytics
            """,
            font=("Arial", 15),
            justify=LEFT,
            bg=self.card_color,
            fg=self.text_color
        ).pack()

        Label(
            self.dashboard,
            text="Developed By Shreyas Goyal",
            font=("Arial", 12, "italic"),
            bg=self.bg_color,
            fg="#94a3b8"
        ).place(
            x=850,
            y=700
        )

        self.update_dashboard_stats()
        self.animate_title()

    def create_sidebar_button(self, text, command):

        btn = Button(
            self.sidebar,
            text=text,
            font=("Arial", 14, "bold"),
            bg=self.sidebar_color,
            fg="white",
            bd=0,
            anchor="w",
            padx=20,
            command=command
        )

        btn.pack(
            fill=X,
            pady=8,
            ipady=12
        )

    def create_card(self, x, y, title, value, color):

        card = Frame(
            self.dashboard,
            bg=self.card_color
        )

        card.place(
            x=x,
            y=y,
            width=280,
            height=170
        )
        Label(
            card,
            text=title,
            font=("Arial", 18, "bold"),
            bg=self.card_color,
            fg=color
        ).pack(pady=20)
        value_lbl = Label(
            card,
            text=value,
            font=("Arial", 40, "bold"),
            bg=self.card_color,
            fg=self.text_color
        )

        value_lbl.pack()

        return value_lbl

    def update_dashboard_stats(self):

        try:

            self.total_students_lbl.config(
                text=str(
                    self.db.get_total_students()
                )
            )

            self.present_students_lbl.config(
                text=str(
                    self.db.get_present_today()
                )
            )

            self.absent_students_lbl.config(
                text=str(
                    self.db.get_absent_today()
                )
            )

        except Exception as e:

            print("Dashboard Error:", e)

        self.root.after(
            3000,
            self.update_dashboard_stats
        )

    def update_clock(self):

        self.clock_lbl.config(
            text=time.strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        )

        self.root.after(
            1000,
            self.update_clock
        )

    def animate_title(self):

        colors = [
            "#38bdf8",
            "#22c55e",
            "#f59e0b",
            "#818cf8"
        ]

        self.title_lbl.config(
            fg=colors[
                int(time.time()) % len(colors)
            ]
        )

        self.root.after(
            500,
            self.animate_title
        )

    def toggle_theme(self):

        self.dark_mode = not self.dark_mode

        if self.dark_mode:

            self.bg_color = self.dark_bg
            self.card_color = self.dark_card
            self.sidebar_color = self.dark_sidebar
            self.text_color = "white"

        else:

            self.bg_color = self.light_bg
            self.card_color = self.light_card
            self.sidebar_color = self.light_sidebar
            self.text_color = "black"

        self.root.configure(bg=self.bg_color)

    def open_register_student(self):

        RegisterStudent(
            Toplevel(self.root)
        )

    def open_face_recognition(self):

        FaceRecognition(
            Toplevel(self.root)
        )

    def open_attendance(self):

        AttendanceSystem(
            Toplevel(self.root)
        )

    def exit_app(self):

        self.root.destroy()


if __name__ == "__main__":

    root = Tk()

    app = FaceAttendanceSystem(root)

    root.mainloop()
