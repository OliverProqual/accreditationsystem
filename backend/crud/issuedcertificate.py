from db import db
from models.issuedcertificate import IssuedCertificateCreate, IssuedCertificate
from fastapi import HTTPException

def create_issued_certificate(cert: IssuedCertificateCreate):
    try:
        with db.cursor() as cursor:
            sql = """
            INSERT INTO issuedcertificates 
            (RegistrationID, CertificateNumber, IssueDate, ExpiryDate, Status)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                cert.RegistrationID,
                cert.CertificateNumber,
                cert.IssueDate,
                cert.ExpiryDate,
                cert.Status
            ))
            db.commit()
            return IssuedCertificate(IssueID=cursor.lastrowid, **cert.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_issued_certificate(issue_id: int):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM issuedcertificates WHERE IssueID=%s", (issue_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Issued certificate not found")
        return IssuedCertificate(
            IssueID=row[0],
            RegistrationID=row[1],
            CertificateNumber=row[2],
            IssueDate=row[3],
            ExpiryDate=row[4],
            Status=row[5]
        )


def list_issued_certificates(limit: int = 10):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM issuedcertificates LIMIT %s", (limit,))
        rows = cursor.fetchall()
        return [
            IssuedCertificate(
                IssueID=row[0],
                RegistrationID=row[1],
                CertificateNumber=row[2],
                IssueDate=row[3],
                ExpiryDate=row[4],
                Status=row[5]
            )
            for row in rows
        ]
    
def update_issued_certificate(issue_id: int, cert: IssuedCertificateCreate):
    try:
        with db.cursor() as cursor:
            sql = """
            UPDATE issuedcertificates
            SET RegistrationID=%s, CertificateNumber=%s, IssueDate=%s, ExpiryDate=%s, Status=%s
            WHERE IssueID=%s
            """
            cursor.execute(sql, (
                cert.RegistrationID,
                cert.CertificateNumber,
                cert.IssueDate,
                cert.ExpiryDate,
                cert.Status,
                issue_id
            ))
            db.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Issued certificate not found")
            return IssuedCertificate(IssueID=issue_id, **cert.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_issued_certificate(issue_id: int):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM issuedcertificates WHERE IssueID=%s", (issue_id,))
            db.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Issued certificate not found")
            return {"status": "deleted", "IssueID": issue_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))