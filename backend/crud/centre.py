from db import db
from models.centre import CentreCreate, Centre
from fastapi import HTTPException

def create_centre(centre: CentreCreate) -> Centre:
    try:
        with db.cursor() as cursor:
            sql = """
            INSERT INTO centres (CentreName, Address, ContactEmail, ContactPhone, IsActive)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                centre.CentreName,
                centre.Address,
                centre.ContactEmail,
                centre.ContactPhone,
                centre.IsActive
            ))
            db.commit()
            return Centre(CentreID=cursor.lastrowid, **centre.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_centre(centre_id: int) -> Centre:
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM centres WHERE CentreID=%s", (centre_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Centre not found")
        return Centre(
            CentreID=row[0],
            CentreName=row[1],
            Address=row[2],
            ContactEmail=row[3],
            ContactPhone=row[4],
            IsActive=row[5]
        )

def update_centre(centre_id: int, centre: CentreCreate):
    try:
        with db.cursor() as cursor:
            sql = """
            UPDATE centres
            SET CentreName=%s, Address=%s, ContactEmail=%s, ContactPhone=%s, IsActive=%s
            WHERE CentreID=%s
            """
            cursor.execute(sql, (
                centre.CentreName,
                centre.Address,
                centre.ContactEmail,
                centre.ContactPhone,
                centre.IsActive,
                centre_id
            ))
            db.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Centre not found")
            return Centre(CentreID=centre_id, **centre.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_centre(centre_id: int):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM centres WHERE CentreID=%s", (centre_id,))
            db.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Centre not found")
            return {"status": "deleted", "CentreID": centre_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
