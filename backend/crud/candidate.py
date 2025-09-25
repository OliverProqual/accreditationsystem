from db import db
from models.candidate import CandidateCreate, Candidate
from fastapi import HTTPException

def list_candidates():
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM candidates")
        return cursor.fetchall()

def get_candidate(candidate_id: int):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM candidates WHERE CandidateID=%s", (candidate_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Candidate not found")
        return result

def create_candidate(candidate: Candidate):
    with db.cursor() as cursor:
        sql = """INSERT INTO candidates (PersonUID, FirstName, LastName, NINumber, Gender, Ethnicity, DateOfBirth, CentreID)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (
            candidate.PersonUID, candidate.FirstName, candidate.LastName,
            candidate.NINumber, candidate.Gender, candidate.Ethnicity,
            candidate.DateOfBirth, candidate.CentreID
        ))
        db.commit()
        candidate.CandidateID = cursor.lastrowid
    return candidate


def update_candidate(candidate_id: int, candidate: CandidateCreate):
    try:
        with db.cursor() as cursor:
            sql = """
            UPDATE candidates
            SET PersonUID=%s, FirstName=%s, LastName=%s, NINumber=%s, Gender=%s, Ethnicity=%s, DateOfBirth=%s, CentreID=%s
            WHERE CandidateID=%s
            """
            cursor.execute(sql, (
                candidate.PersonUID,
                candidate.FirstName,
                candidate.LastName,
                candidate.NINumber,
                candidate.Gender,
                candidate.Ethnicity,
                candidate.DateOfBirth,
                candidate.CentreID,
                candidate_id
            ))
            db.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Candidate not found")
            return Candidate(CandidateID=candidate_id, **candidate.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_candidate(candidate_id: int):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM candidates WHERE CandidateID=%s", (candidate_id,))
            db.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Candidate not found")
            return {"status": "deleted", "CandidateID": candidate_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))