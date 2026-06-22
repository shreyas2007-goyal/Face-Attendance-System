from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

import cv2
import csv
import os

from datetime import datetime
from deepface import DeepFace

from database import DatabaseManager


class AttendanceSystem:

    def __init__(self, root):

        self.root = root

        self.root.geometry("1000x700+200+30")
        self.root.title("Attendance System")
        self.root.config(bg="white")

        self.db = DatabaseManager()

        # FIXED VARIABLE
        self.var_closing_time = StringVar()

        # =========================
        # TITLE
        # =========================

        title_lbl = Label(
            self.root,
            text="ATTENDANCE SYSTEM",
            font=("Arial", 28, "bold"),
            bg="navy",
            fg="white"
        )

        title_lbl.pack(fill=X)

        # =========================
        # TOP FRAME
        # =========================

        top_frame = Frame(
            self.root,
            bg="white",
            bd=3,
            relief=RIDGE
        )

        top_frame.place(
            x=40,
            y=90,
            width=900,
            height=170
        )

        Label(
            top_frame,
            text="Attendance Closing Time",
            font=("Arial", 14, "bold"),
            bg="white"
        ).place(
            x=40,
            y=40
        )

        Entry(
            top_frame,
            textvariable=self.var_closing_time,
            font=("Arial", 14)
        ).place(
            x=320,
            y=40,
            width=180
        )

        Label(
            top_frame,
            text="Example : 09:30",
            font=("Arial", 11),
            bg="white",
            fg="gray"
        ).place(
            x=320,
            y=75
        )

        Button(
            top_frame,
            text="Take Attendance",
            font=("Arial", 15, "bold"),
            bg="green",
            fg="white",
            command=self.take_attendance
        ).place(
            x=120,
            y=110,
            width=220,
            height=45
        )

        Button(
            top_frame,
            text="Download Attendance",
            font=("Arial", 15, "bold"),
            bg="blue",
            fg="white",
            command=self.download_attendance
        ).place(
            x=500,
            y=110,
            width=250,
            height=45
        )

        # =========================
        # TABLE FRAME
        # =========================

        table_frame = Frame(
            self.root,
            bd=3,
            relief=RIDGE
        )

        table_frame.place(
            x=40,
            y=300,
            width=900,
            height=320
        )

        scroll_x = Scrollbar(
            table_frame,
            orient=HORIZONTAL
        )

        scroll_y = Scrollbar(
            table_frame,
            orient=VERTICAL
        )

        self.attendance_table = ttk.Treeview(
            table_frame,
            columns=(
                "name",
                "date",
                "time",
                "status"
            ),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(
            side=BOTTOM,
            fill=X
        )

        scroll_y.pack(
            side=RIGHT,
            fill=Y
        )

        scroll_x.config(
            command=self.attendance_table.xview
        )

        scroll_y.config(
            command=self.attendance_table.yview
        )

        self.attendance_table.heading(
            "name",
            text="Student Name"
        )

        self.attendance_table.heading(
            "date",
            text="Date"
        )

        self.attendance_table.heading(
            "time",
            text="Time"
        )

        self.attendance_table.heading(
            "status",
            text="Status"
        )

        self.attendance_table["show"] = "headings"

        self.attendance_table.column(
            "name",
            width=250
        )

        self.attendance_table.column(
            "date",
            width=150
        )

        self.attendance_table.column(
            "time",
            width=150
        )

        self.attendance_table.column(
            "status",
            width=150
        )

        self.attendance_table.pack(
            fill=BOTH,
            expand=True
        )

        self.load_attendance()

    # =========================
    # LOAD ATTENDANCE
    # =========================

    def load_attendance(self):

        for row in self.attendance_table.get_children():
            self.attendance_table.delete(row)

        records = self.db.get_attendance_records()

        for record in records:

            self.attendance_table.insert(
                "",
                END,
                values=record
            )

    # =========================
    # TAKE ATTENDANCE
    # =========================

    def take_attendance(self):

        closing_time = self.var_closing_time.get().strip()

        if closing_time == "":

            messagebox.showerror(
                "Error",
                "Please Enter Closing Time"
            )

            return

        if not os.path.exists("dataset"):

            messagebox.showerror(
                "Error",
                "Dataset Folder Not Found"
            )

            return

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():

            messagebox.showerror(
                "Error",
                "Unable To Open Camera"
            )

            return

        marked_students = []

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            cv2.imwrite(
                "temp.jpg",
                frame
            )

            detected_name = "Scanning..."
            color = (0, 0, 255)

            try:

                result = DeepFace.find(
                    img_path="temp.jpg",
                    db_path="dataset",
                    model_name="Facenet512",
                    detector_backend="opencv",
                    enforce_detection=False,
                    silent=True
                )

                if len(result[0]) > 0:

                    identity = result[0].iloc[0]["identity"]

                    identity = identity.replace(
                        "\\",
                        "/"
                    )

                    detected_name = identity.split("/")[-2]

                    color = (0, 255, 0)

                    if detected_name not in marked_students:

                        marked_students.append(
                            detected_name
                        )

                        current_time = datetime.now()

                        current_time_str = current_time.strftime(
                            "%H:%M"
                        )

                        full_date = current_time.strftime(
                            "%d-%m-%Y"
                        )

                        full_time = current_time.strftime(
                            "%H:%M:%S"
                        )

                        if current_time_str <= closing_time:

                            status = "Present"

                        else:

                            status = "Late"

                        self.db.mark_attendance(
                            detected_name,
                            status
                        )

                        self.attendance_table.insert(
                            "",
                            END,
                            values=(
                                detected_name,
                                full_date,
                                full_time,
                                status
                            )
                        )

                else:

                    detected_name = "Unknown Face"

            except Exception as e:

                print(e)

                detected_name = "Unknown Face"

            cv2.putText(
                frame,
                detected_name,
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                color,
                2
            )

            cv2.imshow(
                "Attendance System",
                frame
            )

            key = cv2.waitKey(1)

            if key == 13:
                break

        cap.release()

        cv2.destroyAllWindows()

        if os.path.exists("temp.jpg"):
            os.remove("temp.jpg")

        self.load_attendance()

        messagebox.showinfo(
            "Success",
            "Attendance Recorded Successfully"
        )

    # =========================
    # EXPORT CSV
    # =========================

    def download_attendance(self):

        records = self.db.get_attendance_records()

        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV Files", "*.csv")
            ]
        )

        if not save_path:
            return

        with open(
            save_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Student Name",
                "Date",
                "Time",
                "Status"
            ])

            for row in records:
                writer.writerow(row)

        messagebox.showinfo(
            "Success",
            "Attendance Exported Successfully"
        )


if __name__ == "__main__":

    root = Tk()

    app = AttendanceSystem(root)

    root.mainloop()