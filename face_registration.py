from tkinter import *
from tkinter import messagebox
import cv2
import os
import threading
from deepface import DeepFace # type: ignore

class FaceRecognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("750x500+300+100")
        self.root.title("Face Recognition")
        self.root.config(bg="white")
 
        # CAMERA CONTROL VARIABLE
        self.camera_running = False

        # TITLE
        title_lbl = Label(
            self.root,
            text="FACE RECOGNITION SYSTEM",
            font=("times new roman", 30, "bold"),
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

        # INFO LABEL
        info_lbl = Label(
            main_frame,
            text=(
                "• DeepFace Real-Time Recognition\n"
                "• Detects Registered Students\n"
                "• Green = Registered Face\n"
                "• Red = Unknown Face\n"
                "• ENTER Key To Stop\n"
                "• Close Camera Button Added"
            ),
            font=("Arial", 15),
            bg="white",
            fg="gray",
            justify=LEFT
        )
        info_lbl.pack(pady=20)

        # START BUTTON

        start_btn = Button(
            main_frame,
            text="Start Recognition",
            font=("Arial", 16, "bold"),
            bg="green",
            fg="white",
            cursor="hand2",
            command=self.start_thread
        )
        start_btn.pack(
            pady=15,
            ipadx=20,
            ipady=8
        )

        # CLOSE BUTTON
        close_btn = Button(
            main_frame,
            text="Close Camera",
            font=("Arial", 16, "bold"),
            bg="red",
            fg="white",
            cursor="hand2",
            command=self.stop_camera
        )
        close_btn.pack(
            pady=10,
            ipadx=20,
            ipady=8
        )

    # START THREAD
    def start_thread(self):
        threading.Thread(
            target=self.start_recognition,
            daemon=True
        ).start()

    # STOP CAMERA
    def stop_camera(self):
        self.camera_running = False

    # START FACE RECOGNITION
    def start_recognition(self):

        # CHECK DATASET
        if not os.path.exists("dataset"):
            messagebox.showerror(
                "Error",
                "Dataset Folder Not Found"
            )
            return

        # OPEN CAMERA
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror(
                "Error",
                "Unable To Open Camera"
            )
            return

        # START CAMERA LOOP
        self.camera_running = True
        while self.camera_running:
            ret, frame = cap.read()
            if not ret:
                break

            # SAVE TEMP IMAGE
            cv2.imwrite(
                "temp.jpg",
                frame
            )
            detected_name = "Scanning Face..."
            color = (0, 0, 255)
            try:

                # DEEPFACE SEARCH
                result = DeepFace.find(
                    img_path="temp.jpg",
                    db_path="dataset",
                    model_name="Facenet512",
                    detector_backend="opencv",
                    distance_metric="cosine",
                    enforce_detection=False,
                    silent=True
                )

                # FACE FOUND
                if len(result[0]) > 0:
                    identity = result[0].iloc[0]["identity"]
                    identity = identity.replace("\\","/")
                    detected_name = identity.split("/")[-2]
                    color = (0, 255, 0)
                else:
                    detected_name = "Unknown Face"
                    color = (0, 0, 255)
            except Exception as error:
                detected_name = "Unknown Face"
                color = (0, 0, 255)
                print(error)

            # SHOW RESULT
            cv2.putText(
                frame,
                detected_name,
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                color,
                2
            )

            # SHOW CAMERA
            cv2.imshow(
                "Face Recognition",
                frame
            )

            # ENTER KEY TO EXIT
            key = cv2.waitKey(1)
            if key == 13:
                self.camera_running = False
                break

        # RELEASE CAMERA
        cap.release()
        cv2.destroyAllWindows()

        # DELETE TEMP IMAGE
        if os.path.exists("temp.jpg"):
            os.remove("temp.jpg")