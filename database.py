import sqlite3
from datetime import datetime


class DatabaseManager:

    def __init__(self):

        self.student_db = "students.db"
        self.attendance_db = "attendance.db"

        self.create_student_table()
        self.create_attendance_table()

    # =====================================
    # STUDENT TABLE
    # =====================================

    def create_student_table(self):

        conn = sqlite3.connect(self.student_db)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                registration TEXT UNIQUE,
                department TEXT,
                branch TEXT,
                section TEXT,
                batch TEXT,
                roll TEXT
            )
        """)

        conn.commit()
        conn.close()

    # =====================================
    # ATTENDANCE TABLE
    # =====================================

    def create_attendance_table(self):

        conn = sqlite3.connect(self.attendance_db)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT,
                attendance_date TEXT,
                attendance_time TEXT,
                status TEXT
            )
        """)

        conn.commit()
        conn.close()

    # =====================================
    # ADD STUDENT
    # =====================================

    def add_student(
        self,
        name,
        registration,
        department,
        branch,
        section,
        batch,
        roll
    ):

        conn = sqlite3.connect(self.student_db)
        cursor = conn.cursor()

        try:

            cursor.execute("""
                INSERT INTO students(
                    name,
                    registration,
                    department,
                    branch,
                    section,
                    batch,
                    roll
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                name,
                registration,
                department,
                branch,
                section,
                batch,
                roll
            ))

            conn.commit()

        except sqlite3.IntegrityError:

            raise Exception(
                "Registration Number Already Exists"
            )

        finally:

            conn.close()

    # =====================================
    # TOTAL STUDENTS
    # =====================================

    def get_total_students(self):

        conn = sqlite3.connect(self.student_db)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM students"
        )

        total = cursor.fetchone()[0]

        conn.close()

        return total

    # =====================================
    # MARK ATTENDANCE
    # =====================================

    def mark_attendance(
        self,
        student_name,
        status
    ):

        today = datetime.now().strftime("%d-%m-%Y")
        current_time = datetime.now().strftime("%H:%M:%S")

        conn = sqlite3.connect(self.attendance_db)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM attendance
            WHERE student_name=?
            AND attendance_date=?
        """, (
            student_name,
            today
        ))

        record = cursor.fetchone()

        if record is None:

            cursor.execute("""
                INSERT INTO attendance(
                    student_name,
                    attendance_date,
                    attendance_time,
                    status
                )
                VALUES (?, ?, ?, ?)
            """, (
                student_name,
                today,
                current_time,
                status
            ))

            conn.commit()

        conn.close()

    # =====================================
    # PRESENT TODAY
    # =====================================

    def get_present_today(self):

        today = datetime.now().strftime("%d-%m-%Y")

        conn = sqlite3.connect(self.attendance_db)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE attendance_date=?
            AND status='Present'
        """, (today,))

        count = cursor.fetchone()[0]

        conn.close()

        return count

    # =====================================
    # LATE TODAY
    # =====================================

    def get_late_today(self):

        today = datetime.now().strftime("%d-%m-%Y")

        conn = sqlite3.connect(self.attendance_db)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE attendance_date=?
            AND status='Late'
        """, (today,))

        count = cursor.fetchone()[0]

        conn.close()

        return count

    # =====================================
    # ABSENT TODAY
    # =====================================

    def get_absent_today(self):

        total = self.get_total_students()
        present = self.get_present_today()
        late = self.get_late_today()

        absent = total - (present + late)

        return max(0, absent)

    # =====================================
    # ALL ATTENDANCE
    # =====================================

    def get_attendance_records(self):

        conn = sqlite3.connect(self.attendance_db)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                student_name,
                attendance_date,
                attendance_time,
                status
            FROM attendance
            ORDER BY id DESC
        """)

        records = cursor.fetchall()

        conn.close()

        return records