from tkinter import *
from tkinter import messagebox

from add_face import AddFace
from database import DatabaseManager


class RegisterStudent:

    def __init__(self, root):

        self.root = root

        self.root.geometry("900x650+250+50")

        self.root.title("Register Student")

        self.root.config(bg="white")

        # DATABASE

        self.db = DatabaseManager()

        # VARIABLES

        self.var_name = StringVar()

        self.var_reg = StringVar()

        self.var_department = StringVar()

        self.var_branch = StringVar()

        self.var_section = StringVar()

        self.var_batch = StringVar()

        self.var_roll = StringVar()

        # TITLE

        title_lbl = Label(
            self.root,
            text="STUDENT REGISTRATION",
            font=("Arial", 26, "bold"),
            bg="navy",
            fg="white"
        )

        title_lbl.pack(fill=X)

        # MAIN FRAME

        main_frame = Frame(
            self.root,
            bg="white",
            bd=3,
            relief=RIDGE
        )

        main_frame.place(
            x=80,
            y=100,
            width=740,
            height=450
        )

        label_font = (
            "Arial",
            14,
            "bold"
        )

        # NAME

        Label(
            main_frame,
            text="Student Name",
            font=label_font,
            bg="white"
        ).place(x=50, y=40)

        Entry(
            main_frame,
            textvariable=self.var_name,
            font=("Arial", 14)
        ).place(x=250, y=40, width=300)

        # REGISTRATION

        Label(
            main_frame,
            text="Registration No",
            font=label_font,
            bg="white"
        ).place(x=50, y=100)

        Entry(
            main_frame,
            textvariable=self.var_reg,
            font=("Arial", 14)
        ).place(x=250, y=100, width=300)

        # DEPARTMENT

        Label(
            main_frame,
            text="Department",
            font=label_font,
            bg="white"
        ).place(x=50, y=160)

        Entry(
            main_frame,
            textvariable=self.var_department,
            font=("Arial", 14)
        ).place(x=250, y=160, width=300)

        # BRANCH

        Label(
            main_frame,
            text="Branch",
            font=label_font,
            bg="white"
        ).place(x=50, y=220)

        Entry(
            main_frame,
            textvariable=self.var_branch,
            font=("Arial", 14)
        ).place(x=250, y=220, width=300)

        # SECTION

        Label(
            main_frame,
            text="Section",
            font=label_font,
            bg="white"
        ).place(x=50, y=280)

        Entry(
            main_frame,
            textvariable=self.var_section,
            font=("Arial", 14)
        ).place(x=250, y=280, width=300)

        # BATCH

        Label(
            main_frame,
            text="Batch",
            font=label_font,
            bg="white"
        ).place(x=50, y=340)

        Entry(
            main_frame,
            textvariable=self.var_batch,
            font=("Arial", 14)
        ).place(x=250, y=340, width=300)

        # ROLL

        Label(
            main_frame,
            text="Roll Number",
            font=label_font,
            bg="white"
        ).place(x=50, y=400)

        Entry(
            main_frame,
            textvariable=self.var_roll,
            font=("Arial", 14)
        ).place(x=250, y=400, width=300)

        # SAVE BUTTON

        save_btn = Button(
            self.root,
            text="Save Student",
            font=("Arial", 15, "bold"),
            bg="green",
            fg="white",
            cursor="hand2",
            command=self.save_student
        )

        save_btn.place(
            x=220,
            y=580,
            width=200,
            height=50
        )

        # FACE BUTTON

        add_face_btn = Button(
            self.root,
            text="Add Face",
            font=("Arial", 15, "bold"),
            bg="#1f6aa5",
            fg="white",
            cursor="hand2",
            command=self.open_add_face
        )

        add_face_btn.place(
            x=500,
            y=580,
            width=200,
            height=50
        )

    # =====================================
    # SAVE STUDENT
    # =====================================
    def save_student(self):

        if self.var_name.get() == "":
            messagebox.showerror(
                "Error",
                "Please Enter Student Name"
            )
            return

        try:

            self.db.add_student(
                self.var_name.get(),
                self.var_reg.get(),
                self.var_department.get(),
                self.var_branch.get(),
                self.var_section.get(),
                self.var_batch.get(),
                self.var_roll.get()
            )

            print("Student Saved Successfully")
            print("Total Students:", self.db.get_total_students())

            messagebox.showinfo(
                "Success",
                "Student Registered Successfully"
            )

            self.clear_fields()

        except Exception as e:

            print("Database Error:", e)
   
    # =====================================
    # CLEAR FORM
    # =====================================

    def clear_fields(self):

        self.var_name.set("")

        self.var_reg.set("")

        self.var_department.set("")

        self.var_branch.set("")

        self.var_section.set("")

        self.var_batch.set("")

        self.var_roll.set("")

    # =====================================
    # ADD FACE
    # =====================================

    def open_add_face(self):

        if self.var_name.get() == "":

            messagebox.showerror(
                "Error",
                "Please Enter Student Name First"
            )

            return

        new_window = Toplevel(
            self.root
        )

        AddFace(
            new_window,
            self.var_name.get()
        )
