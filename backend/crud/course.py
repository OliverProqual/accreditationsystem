from db import db
from models.course import CourseCreate, Course
from fastapi import HTTPException


def create_course(course: CourseCreate):
    try:
        with db.cursor() as cursor:
            sql = """
            INSERT INTO courses (CourseCode, CourseName, Description, DurationWeeks, CertificateID)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                course.CourseCode,
                course.CourseName,
                course.Description,
                course.DurationWeeks,
                course.CertificateID
            ))
            db.commit()
            return Course(CourseID=cursor.lastrowid, **course.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_course(course_id: int):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM courses WHERE CourseID=%s", (course_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Course not found")
        return Course(
            CourseID=row[0],
            CourseCode=row[1],
            CourseName=row[2],
            Description=row[3],
            DurationWeeks=row[4],
            CertificateID=row[5]
        )


def list_courses(limit: int = 10):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM courses LIMIT %s", (limit,))
        rows = cursor.fetchall()
        return [
            Course(
                CourseID=row[0],
                CourseCode=row[1],
                CourseName=row[2],
                Description=row[3],
                DurationWeeks=row[4],
                CertificateID=row[5]
            )
            for row in rows
        ]
    

def update_course(course_id: int, course: CourseCreate):
    try:
        with db.cursor() as cursor:
            sql = """
            UPDATE courses
            SET CourseCode=%s, CourseName=%s, Description=%s, DurationWeeks=%s, CertificateID=%s
            WHERE CourseID=%s
            """
            cursor.execute(sql, (
                course.CourseCode,
                course.CourseName,
                course.Description,
                course.DurationWeeks,
                course.CertificateID,
                course_id
            ))
            db.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Course not found")
            return Course(CourseID=course_id, **course.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_course(course_id: int):
    try:
        with db.cursor() as cursor:
            sql = "DELETE FROM courses WHERE CourseID=%s"
            cursor.execute(sql, (course_id,))
            db.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Course not found")
            return {"status": "deleted", "CourseID": course_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
