from passlib.context import CryptContext
from db import db  # import your existing DB connection

# same CryptContext as in your auth.py
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def rehash_passwords():
    with db.cursor() as cursor:
        # ⚠️ adjust column names if needed
        cursor.execute("SELECT UserID, PasswordHash FROM users")
        users = cursor.fetchall()

        for user_id, pw in users:
            # bcrypt hashes are usually 60 chars and start with $2b$ or $2a$
            if not (pw.startswith("$2") and len(pw) > 50):
                print(f"Rehashing password for user {user_id}...")
                hashed = get_password_hash(pw)
                cursor.execute(
                    "UPDATE users SET PasswordHash=%s WHERE UserID=%s",
                    (hashed, user_id),
                )

        db.commit()

if __name__ == "__main__":
    rehash_passwords()
    print("✅ Passwords rehashed where needed")
