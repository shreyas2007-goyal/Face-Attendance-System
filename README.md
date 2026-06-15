# Face Attendance System

A modern Face Recognition-Based Attendance Management System built using Python, OpenCV, Tkinter, and SQLite. The system automates attendance tracking by recognizing registered students through facial recognition, reducing manual effort and improving accuracy.

---

## Overview

The Face Attendance System allows institutions and organizations to manage attendance digitally using computer vision. Students can be registered with facial data, trained into the recognition model, and automatically marked present when detected by the camera.

---

## Features

### Student Management

* Register new students
* Store student information securely
* Manage student records

### Face Registration

* Capture facial images using webcam
* Create training datasets automatically
* Store face data for recognition

### Face Recognition Attendance

* Real-time face detection
* Automatic attendance marking
* Duplicate attendance prevention

### Attendance Analytics

* Total registered students
* Present students count
* Absent students count
* Late attendance tracking

### Attendance Records

* Daily attendance logs
* Attendance history
* Export-ready attendance data

### User Interface

* Modern Tkinter dashboard
* Easy navigation
* Real-time statistics display

---

## Tech Stack

| Technology | Purpose                      |
| ---------- | ---------------------------- |
| Python     | Core Programming Language    |
| OpenCV     | Face Detection & Recognition |
| Tkinter    | Graphical User Interface     |
| SQLite     | Database Management          |
| NumPy      | Numerical Operations         |
| Pillow     | Image Processing             |

---

## Project Structure

```text
FACE_ATTENDANCE/
│
├── main.py
├── add_face.py
├── attendance.py
├── database.py
├── face_registration.py
├── register_student.py
├── requirements.txt
├── README.md
└── .gitignore
```
---

## Installation

### Clone the Repository

```bash
git clone https://github.com/shreyas2007-goyal/Face-Attendance-System.git
cd Face-Attendance-System
```

### Create Virtual Environment

```bash
python -m venv penv
```

### Activate Virtual Environment

#### Windows

```bash
penv\Scripts\activate
```

#### Linux / macOS

```bash
source penv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
python main.py
```

---

## Workflow

1. Register a student.
2. Capture facial data.
3. Train the recognition model.
4. Start attendance system.
5. Student face is recognized.
6. Attendance is marked automatically.
7. Dashboard statistics are updated.

---

## Future Improvements

* Cloud database integration
* Multi-camera support
* Face recognition accuracy improvements
* Web dashboard
* Email attendance reports
* QR + Face hybrid attendance
* Admin authentication system

---

## Learning Outcomes

This project demonstrates practical implementation of:

* Computer Vision
* Face Recognition
* Database Management
* GUI Development
* Python Application Development
* Attendance Automation Systems

---

## Author

**Shreyas Goyal**

B.Tech CSE (AI & ML)

Passionate about AI, Computer Vision, Software Development, and building real-world solutions.

---

## License

This project is intended for educational and learning purposes.
