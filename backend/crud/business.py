import pymysql
from fastapi import HTTPException
from typing import List
from models.candidate import Candidate
from models.centre import Centre, CentreCreate
from models.course import Course, CourseCreate
from models.certificate import Certificate, CertificateCreate
from models.cohort import Cohort
from models.user import User
from models.courseregistration import CourseRegistration, CourseRegistrationCreate
from models.issuedcertificate import IssuedCertificate, IssuedCertificateCreate
from routers.auth import TokenData

# ⚡ adjust to your db.py if you have one
db = pymysql.connect(
    host="localhost",
    user="root",
    password="Po1*wk01Grqc^363Igcs47@0yBko7@38",
    database="accreditationsystem",
    cursorclass=pymysql.cursors.DictCursor
)

# ---------------- Candidates ----------------
def list_candidates(current_user: TokenData) -> List[Candidate]:
    with db.cursor() as cursor:
        if current_user.Role == "AccreditationStaff":
            cursor.execute("SELECT * FROM candidates")
        else:
            cursor.execute("SELECT * FROM candidates WHERE CentreID=%s", (current_user.CentreID,))
        rows = cursor.fetchall()
    return [Candidate(**row) for row in rows]

# ---------------- Centres ----------------
def list_centres(current_user: TokenData) -> List[Centre]:
    with db.cursor() as cursor:
        if current_user.Role == "AccreditationStaff":
            cursor.execute("SELECT * FROM centres")
        else:
            cursor.execute("SELECT * FROM centres WHERE CentreID=%s", (current_user.CentreID,))
        rows = cursor.fetchall()
    return [Centre(**row) for row in rows]

# ---------------- Courses ----------------
def list_courses(current_user: TokenData) -> List[Course]:
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM courses")
        rows = cursor.fetchall()
    return [Course(**row) for row in rows]

def create_course(course: CourseCreate, current_user: TokenData) -> Course:
    if current_user.Role != "AccreditationStaff":
        raise HTTPException(status_code=403, detail="Only accreditation staff can create courses")
    with db.cursor() as cursor:
        cursor.execute(
            "INSERT INTO courses (CourseCode, CourseName, Description, DurationWeeks, CertificateID) VALUES (%s, %s, %s, %s, %s)",
            (course.CourseCode, course.CourseName, course.Description, course.DurationWeeks, course.CertificateID)
        )
        db.commit()
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM courses WHERE CourseID=%s", (new_id,))
        row = cursor.fetchone()
    return Course(**row)

# ---------------- Certificates ----------------
def list_certificates(current_user: TokenData) -> List[Certificate]:
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM certificates")
        rows = cursor.fetchall()
    return [Certificate(**row) for row in rows]

def create_certificate(cert: CertificateCreate, current_user: TokenData) -> Certificate:
    if current_user.Role != "AccreditationStaff":
        raise HTTPException(status_code=403, detail="Only accreditation staff can create certificates")
    with db.cursor() as cursor:
        cursor.execute(
            "INSERT INTO certificates (CertificateName, Level, Description) VALUES (%s, %s, %s)",
            (cert.CertificateName, cert.Level, cert.Description)
        )
        db.commit()
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM certificates WHERE CertificateID=%s", (new_id,))
        row = cursor.fetchone()
    return Certificate(**row)

# ---------------- Cohorts ----------------
def list_cohorts(current_user: TokenData) -> List[Cohort]:
    with db.cursor() as cursor:
        if current_user.Role == "AccreditationStaff":
            cursor.execute("SELECT * FROM cohorts")
        else:
            cursor.execute("SELECT * FROM cohorts WHERE CentreID=%s", (current_user.CentreID,))
        rows = cursor.fetchall()
    return [Cohort(**row) for row in rows]

# ---------------- Users ----------------
def list_users(current_user: TokenData) -> List[User]:
    with db.cursor() as cursor:
        if current_user.Role == "AccreditationStaff":
            cursor.execute("SELECT * FROM users")
        else:
            cursor.execute("SELECT * FROM users WHERE CentreID=%s", (current_user.CentreID,))
        rows = cursor.fetchall()
    return [User(**row) for row in rows]

# ---------------- Course Registrations ----------------
def list_registrations(current_user: TokenData) -> List[CourseRegistration]:
    with db.cursor() as cursor:
        if current_user.Role == "AccreditationStaff":
            cursor.execute("SELECT * FROM courseregistrations")
        else:
            cursor.execute(
                "SELECT r.* FROM courseregistrations r JOIN candidates c ON r.CandidateID = c.CandidateID WHERE c.CentreID=%s",
                (current_user.CentreID,)
            )
        rows = cursor.fetchall()
    return [CourseRegistration(**row) for row in rows]

# ---------------- Issued Certificates ----------------
def list_issued_certificates(current_user: TokenData) -> List[IssuedCertificate]:
    with db.cursor() as cursor:
        if current_user.Role == "AccreditationStaff":
            cursor.execute("SELECT * FROM issuedcertificates")

