from tkinter import *
from tkinter import messagebox
import cv2
import os
import time


class AddFace:

    def __init__(self, root, student_name):
        self.root = root
        self.student_name = student_name
        self.root.geometry("750x500+300+100")
        self.root.title("Add Face Dataset")
        self.root.config(bg="white")
        
        # TITLE
        title_lbl = Label(
            self.root,
            text="ADD FACE DATASET",
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
            y=110,
            width=610,
            height=280
        )
       
        # STUDENT NAME
        student_lbl = Label(
            main_frame,
            text=f"Student : {self.student_name}",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="black"
        )
        student_lbl.pack(pady=20)
        
        # INSTRUCTIONS
        instruction_lbl = Label(
            main_frame,
            text=(
                "• Keep your face clearly visible\n"
                "• Slightly move your face in different directions\n"
                "• 50 face images will be captured automatically\n"
                "• Press ENTER to stop anytime"
            ),
            font=("Arial", 14),
            bg="white",
            fg="black",
            justify=LEFT
        )
        instruction_lbl.pack(pady=10)
        
        # START BUTTON
        start_btn = Button(
            main_frame,
            text="Start Capturing Faces",
            font=("Arial", 16, "bold"),
            bg="green",
            fg="white",
            cursor="hand2",
            command=self.capture_faces
        )
        start_btn.pack(
            pady=20,
            ipadx=20,
            ipady=8
        )
    
    # CAPTURE FACE DATASET
    def capture_faces(self):
      
        # CREATE DATASET FOLDER
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

        # FACE DETECTOR
        face_classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

        # CAMERA
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror(
                "Error",
                "Unable To Open Camera"
            )
            return

        img_id = 0
        
        # CAMERA LOOP
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )
            faces = face_classifier.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5
            )

            # FACE DETECTION
            for (x, y, w, h) in faces:
                
                # CROP FACE
                face = frame[
                    y:y+h,
                    x:x+w
                ]

                # RESIZE FACE
                face = cv2.resize(
                    face,
                    (300, 300)
                )
               
                # IMAGE PATH
                img_path = os.path.join(
                    student_folder,
                    f"{img_id}.jpg"
                )
                
                # SAVE IMAGE
                cv2.imwrite(
                    img_path,
                    face
                )
                img_id += 1

               # FACE RECTANGLE
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x+w, y+h),
                    (0, 255, 0),
                    2
                )
               
                # CAPTURE COUNT
                cv2.putText(
                    frame,
                    f"Captured : {img_id}/50",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
                
                # DELAY
                time.sleep(0.1)

            # SHOW CAMERA
            cv2.imshow(
                "Capturing Face Dataset",
                frame
            )

           # ENTER KEY TO STOP
            key = cv2.waitKey(1)
            if key == 13:
                break
            
            # STOP AFTER 50 IMAGES
            if img_id >= 50:
                break
        
        # RELEASE CAMERA
        cap.release()
        cv2.destroyAllWindows()
      
        # SUCCESS MESSAGE
        messagebox.showinfo(
            "Success",
            f"50 Images Captured For {self.student_name}"
        )