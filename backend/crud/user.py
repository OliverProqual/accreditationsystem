from db import db
from models.user import UserCreate, User
from fastapi import HTTPException

def create_user(user: UserCreate):
    try:
        with db.cursor() as cursor:
            sql = """
            INSERT INTO users (CentreID, FirstName, LastName, Email, PasswordHash, Role, IsActive)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                user.CentreID,
                user.FirstName,
                user.LastName,
                user.Email,
                user.PasswordHash,
                user.Role,
                user.IsActive
            ))
            db.commit()
            return User(UserID=cursor.lastrowid, **user.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_user(user_id: int):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE UserID=%s", (user_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        return User(
            UserID=row[0],
            CentreID=row[1],
            FirstName=row[2],
            LastName=row[3],
            Email=row[4],
            PasswordHash=row[5],
            Role=row[6],
            IsActive=bool(row[7])
        )


def list_users(limit: int = 10):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM users LIMIT %s", (limit,))
        rows = cursor.fetchall()
        return [
            User(
                UserID=row[0],
                CentreID=row[1],
                FirstName=row[2],
                LastName=row[3],
                Email=row[4],
                PasswordHash=row[5],
                Role=row[6],
                IsActive=bool(row[7])
            )
            for row in rows
        ]
    

def update_user(user_id: int, user: UserCreate):
    try:
        with db.cursor() as cursor:
            sql = """
            UPDATE users
            SET CentreID=%s, FirstName=%s, LastName=%s, Email=%s, PasswordHash=%s, Role=%s, IsActive=%s
            WHERE UserID=%s
            """
            cursor.execute(sql, (
                user.CentreID,
                user.FirstName,
                user.LastName,
                user.Email,
                user.PasswordHash,
                user.Role,
                user.IsActive,
                user_id
            ))
            db.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")
            return User(UserID=user_id, **user.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_user(user_id: int):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE UserID=%s", (user_id,))
            db.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")
            return {"status": "deleted", "UserID": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

