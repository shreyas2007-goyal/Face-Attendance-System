from tkinter import *
from tkinter import messagebox
import cv2
import os


class AddFace:

    def __init__(self, root, student_name):

        self.root = root
        self.student_name = student_name

        self.root.geometry("750x500+300+100")
        self.root.title("Add Face Dataset")
        self.root.config(bg="white")

        title_lbl = Label(
            self.root,
            text="ADD FACE DATASET",
            font=("Arial", 28, "bold"),
            bg="navy",
            fg="white"
        )

        title_lbl.pack(fill=X)

        main_frame = Frame(
            self.root,
            bg="white",
            bd=3,
            relief=RIDGE
        )

        main_frame.place(
            x=70,
            y=110,
            width=610,
            height=280
        )

        Label(
            main_frame,
            text=f"Student : {self.student_name}",
            font=("Arial", 18, "bold"),
            bg="white"
        ).pack(pady=20)

        Label(
            main_frame,
            text=(
                "• Keep your face clearly visible\n"
                "• Look left and right\n"
                "• Look up and down\n"
                "• Dataset will capture 50 images\n"
                "• Press ENTER to stop"
            ),
            font=("Arial", 14),
            bg="white",
            justify=LEFT
        ).pack(pady=10)

        Button(
            main_frame,
            text="Start Capturing Faces",
            font=("Arial", 16, "bold"),
            bg="green",
            fg="white",
            cursor="hand2",
            command=self.capture_faces
        ).pack(
            pady=20,
            ipadx=20,
            ipady=8
        )

    # =====================================
    # CAPTURE FACE DATASET
    # =====================================

    def capture_faces(self):

        os.makedirs(
            "dataset",
            exist_ok=True
        )

        student_folder = os.path.join(
            "dataset",
            self.student_name
        )

        os.makedirs(
            student_folder,
            exist_ok=True
        )

        face_detector = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():

            messagebox.showerror(
                "Camera Error",
                "Unable To Open Camera"
            )

            return

        img_id = 0

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            faces = face_detector.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5
            )

            for (x, y, w, h) in faces:

                face = frame[
                    y:y+h,
                    x:x+w
                ]

                face = cv2.resize(
                    face,
                    (224, 224)
                )

                img_path = os.path.join(
                    student_folder,
                    f"{img_id}.jpg"
                )

                cv2.imwrite(
                    img_path,
                    face
                )

                img_id += 1

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x+w, y+h),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Captured: {img_id}/50",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

            cv2.imshow(
                "Capturing Face Dataset",
                frame
            )

            key = cv2.waitKey(50)

            if key == 13:
                break

            if img_id >= 50:
                break

        cap.release()

        cv2.destroyAllWindows()

        messagebox.showinfo(
            "Success",
            f"{img_id} Images Captured Successfully"
        )


if __name__ == "__main__":

    root = Tk()

    app = AddFace(
        root,
        "Test Student"
    )

    root.mainloop()