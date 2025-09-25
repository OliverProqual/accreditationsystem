from db import db
from models.certificate import CertificateCreate, Certificate
from fastapi import HTTPException

def create_certificate(cert: CertificateCreate):
    try:
        with db.cursor() as cursor:
            sql = """
            INSERT INTO certificates (CertificateName, Level, Description)
            VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (
                cert.CertificateName,
                cert.Level,
                cert.Description
            ))
            db.commit()
            return Certificate(CertificateID=cursor.lastrowid, **cert.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_certificate(certificate_id: int):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM certificates WHERE CertificateID=%s", (certificate_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Certificate not found")
        return Certificate(
            CertificateID=row[0],
            CertificateName=row[1],
            Level=row[2],
            Description=row[3]
        )


def list_certificates(limit: int = 10):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM certificates LIMIT %s", (limit,))
        rows = cursor.fetchall()
        return [
            Certificate(
                CertificateID=row[0],
                CertificateName=row[1],
                Level=row[2],
                Description=row[3]
            )
            for row in rows
        ]
    
def update_certificate(certificate_id: int, cert: CertificateCreate):
    try:
        with db.cursor() as cursor:
            sql = """
            UPDATE certificates
            SET CertificateName=%s, Level=%s, Description=%s
            WHERE CertificateID=%s
            """
            cursor.execute(sql, (
                cert.CertificateName,
                cert.Level,
                cert.Description,
                certificate_id
            ))
            db.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Certificate not found")
            return Certificate(CertificateID=certificate_id, **cert.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_certificate(certificate_id: int):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM certificates WHERE CertificateID=%s", (certificate_id,))
            db.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Certificate not found")
            return {"status": "deleted", "CertificateID": certificate_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))