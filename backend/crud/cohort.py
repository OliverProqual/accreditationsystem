from db import db
from models.cohort import CohortCreate, Cohort
from fastapi import HTTPException

def create_cohort(cohort: CohortCreate):
    try:
        with db.cursor() as cursor:
            sql = """
            INSERT INTO cohorts (CentreID, CourseID, InstructorID, StartDate, EndDate)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                cohort.CentreID,
                cohort.CourseID,
                cohort.InstructorID,
                cohort.StartDate,
                cohort.EndDate
            ))
            db.commit()
            return Cohort(CohortID=cursor.lastrowid, **cohort.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_cohort(cohort_id: int):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM cohorts WHERE CohortID=%s", (cohort_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Cohort not found")
        return Cohort(
            CohortID=row[0],
            CentreID=row[1],
            CourseID=row[2],
            InstructorID=row[3],
            StartDate=row[4],
            EndDate=row[5]
        )


def list_cohorts(limit: int = 10):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM cohorts LIMIT %s", (limit,))
        rows = cursor.fetchall()
        return [
            Cohort(
                CohortID=row[0],
                CentreID=row[1],
                CourseID=row[2],
                InstructorID=row[3],
                StartDate=row[4],
                EndDate=row[5]
            )
            for row in rows
        ]
    
def update_cohort(cohort_id: int, cohort: CohortCreate):
    try:
        with db.cursor() as cursor:
            sql = """
            UPDATE cohorts
            SET CentreID=%s, CourseID=%s, InstructorID=%s, StartDate=%s, EndDate=%s
            WHERE CohortID=%s
            """
            cursor.execute(sql, (
                cohort.CentreID,
                cohort.CourseID,
                cohort.InstructorID,
                cohort.StartDate,
                cohort.EndDate,
                cohort_id
            ))
            db.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Cohort not found")
            return Cohort(CohortID=cohort_id, **cohort.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_cohort(cohort_id: int):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM cohorts WHERE CohortID=%s", (cohort_id,))
            db.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Cohort not found")
            return {"status": "deleted", "CohortID": cohort_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))