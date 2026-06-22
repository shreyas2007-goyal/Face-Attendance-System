from tkinter import *
from tkinter import messagebox
import cv2
import os
import threading
from deepface import DeepFace


class FaceRecognition:

    def __init__(self, root):

        self.root = root

        self.root.geometry("750x500+300+100")
        self.root.title("Face Recognition")
        self.root.config(bg="white")

        self.camera_running = False

        # TITLE

        title_lbl = Label(
            self.root,
            text="FACE RECOGNITION SYSTEM",
            font=("Arial", 28, "bold"),
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
            x=70,
            y=120,
            width=610,
            height=280
        )

        # INFO

        Label(
            main_frame,
            text=(
                "• Real-Time Face Recognition\n"
                "• Detect Registered Students\n"
                "• Green = Registered Face\n"
                "• Red = Unknown Face\n"
                "• Press ENTER To Stop Camera"
            ),
            font=("Arial", 14),
            bg="white",
            fg="gray",
            justify=LEFT
        ).pack(pady=20)

        # START BUTTON

        Button(
            main_frame,
            text="Start Recognition",
            font=("Arial", 16, "bold"),
            bg="green",
            fg="white",
            cursor="hand2",
            command=self.start_thread
        ).pack(
            pady=15,
            ipadx=20,
            ipady=8
        )

        # STOP BUTTON

        Button(
            main_frame,
            text="Close Camera",
            font=("Arial", 16, "bold"),
            bg="red",
            fg="white",
            cursor="hand2",
            command=self.stop_camera
        ).pack(
            pady=10,
            ipadx=20,
            ipady=8
        )

    # =====================================
    # THREAD START
    # =====================================

    def start_thread(self):

        threading.Thread(
            target=self.start_recognition,
            daemon=True
        ).start()

    # =====================================
    # STOP CAMERA
    # =====================================

    def stop_camera(self):

        self.camera_running = False

    # =====================================
    # FACE RECOGNITION
    # =====================================

    def start_recognition(self):

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

        self.camera_running = True

        while self.camera_running:

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
                    distance_metric="cosine",
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

                else:

                    detected_name = "Unknown Face"

            except Exception as error:

                print(error)

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
                "Face Recognition",
                frame
            )

            key = cv2.waitKey(1)

            if key == 13:

                self.camera_running = False
                break

        cap.release()

        cv2.destroyAllWindows()

        if os.path.exists("temp.jpg"):

            os.remove("temp.jpg")


if __name__ == "__main__":

    root = Tk()

    app = FaceRecognition(root)

    root.mainloop()