from db import db
from models.courseregistration import CourseRegistrationCreate, CourseRegistration
from fastapi import HTTPException

def create_registration(reg: CourseRegistrationCreate):
    try:
        with db.cursor() as cursor:
            sql = """
            INSERT INTO courseregistrations 
            (CandidateID, CohortID, RegistrationDate, PaymentStatus, Status, Result, CompletionDate)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                reg.CandidateID,
                reg.CohortID,
                reg.RegistrationDate,
                reg.PaymentStatus,
                reg.Status,
                reg.Result,
                reg.CompletionDate
            ))
            db.commit()
            return CourseRegistration(RegistrationID=cursor.lastrowid, **reg.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_registration(registration_id: int):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM courseregistrations WHERE RegistrationID=%s", (registration_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Registration not found")
        return CourseRegistration(
            RegistrationID=row[0],
            CandidateID=row[1],
            CohortID=row[2],
            RegistrationDate=row[3],
            PaymentStatus=row[4],
            Status=row[5],
            Result=row[6],
            CompletionDate=row[7]
        )


def list_registrations(limit: int = 10):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM courseregistrations LIMIT %s", (limit,))
        rows = cursor.fetchall()
        return [
            CourseRegistration(
                RegistrationID=row[0],
                CandidateID=row[1],
                CohortID=row[2],
                RegistrationDate=row[3],
                PaymentStatus=row[4],
                Status=row[5],
                Result=row[6],
                CompletionDate=row[7]
            )
            for row in rows
        ]