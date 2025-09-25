from fastapi import FastAPI, HTTPException, Depends, Path
from pydantic import BaseModel
import pymysql
from typing import Optional
from datetime import date
from typing import List

db = pymysql.connect(
    host="localhost",
    user="root",
    password="Po1*wk01Grqc^363Igcs47@0yBko7@38",
    database="accreditationsystem"
)

from typing import Optional
from pydantic import BaseModel
from datetime import date

# ---- Candidates ----
class CandidateBase(BaseModel):
    PersonUID: str
    FirstName: str
    LastName: str
    NINumber: Optional[str] = None
    Gender: Optional[str] = None
    Ethnicity: Optional[str] = None
    DateOfBirth: Optional[date] = None
    CentreID: int

class CandidateCreate(CandidateBase):
    pass

class Candidate(CandidateBase):
    CandidateID: int

    class Config:
        orm_mode = True

class CertificateBase(BaseModel):
    CertificateName: str
    Level: Optional[str] = None
    Description: Optional[str] = None

class CertificateCreate(CertificateBase):
    pass

class Certificate(CertificateBase):
    CertificateID: int

    class Config:
        orm_mode = True

class CourseBase(BaseModel):
    CourseCode: str
    CourseName: str
    Description: Optional[str] = None
    DurationWeeks: Optional[int] = None
    CertificateID: int

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    CourseID: int

    class Config:
        orm_mode = True

class CohortBase(BaseModel):
    CentreID: int
    CourseID: int
    InstructorID: Optional[int] = None
    StartDate: date
    EndDate: Optional[date] = None

class CohortCreate(CohortBase):
    pass

class Cohort(CohortBase):
    CohortID: int

    class Config:
        orm_mode = True

class CourseRegistrationBase(BaseModel):
    CandidateID: int
    CohortID: int
    RegistrationDate: date
    PaymentStatus: Optional[str] = "Pending"     # Pending, Paid, Failed
    Status: Optional[str] = "Registered"         # Registered, InProgress, Completed, Withdrawn
    Result: Optional[str] = None
    CompletionDate: Optional[date] = None

class CourseRegistrationCreate(CourseRegistrationBase):
    pass

class CourseRegistration(CourseRegistrationBase):
    RegistrationID: int

    class Config:
        orm_mode = True

class IssuedCertificateBase(BaseModel):
    RegistrationID: int
    CertificateNumber: str
    IssueDate: date
    ExpiryDate: Optional[date] = None
    Status: Optional[str] = "Valid"   # Valid, Expired, Revoked

class IssuedCertificateCreate(IssuedCertificateBase):
    pass

class IssuedCertificate(IssuedCertificateBase):
    IssueID: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    CentreID: Optional[int] = None
    FirstName: str
    LastName: str
    Email: str
    PasswordHash: str  # normally you'd hash this properly!
    Role: str  # must be one of: AccreditationStaff, CentreStaff, Instructor
    IsActive: Optional[bool] = True

class UserCreate(UserBase):
    pass

class User(UserBase):
    UserID: int

    class Config:
        orm_mode = True

class CentreBase(BaseModel):
    CentreName: str
    Address: Optional[str] = None
    ContactEmail: Optional[str] = None
    ContactPhone: Optional[str] = None
    IsActive: Optional[bool] = True

class CentreCreate(CentreBase):
    pass

class Centre(CentreBase):
    CentreID: int

    class Config:
        orm_mode = True

app = FastAPI()

@app.get("/candidates", response_model=List[Candidate])
def list_candidates():
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM candidates")
        return cursor.fetchall()

@app.get("/candidates/{candidate_id}", response_model=Candidate)
def get_candidate(candidate_id: int):
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM candidates WHERE CandidateID=%s", (candidate_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Candidate not found")
        return result

@app.post("/candidates", response_model=Candidate)
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

@app.put("/candidates/{candidate_id}", response_model=Candidate)
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


@app.delete("/candidates/{candidate_id}")
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


@app.get("/centres", response_model=List[Centre])
def list_centres():
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM centres")
        return cursor.fetchall()

@app.get("/centres/{centre_id}", response_model=Centre)
def get_centre(centre_id: int):
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM centres WHERE CentreID=%s", (centre_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Centre not found")
        return result

@app.post("/centres", response_model=Centre)
def create_centre(centre: Centre):
    with db.cursor() as cursor:
        sql = """INSERT INTO centres (CentreName, Address, ContactEmail, ContactPhone, IsActive)
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (
            centre.CentreName, centre.Address,
            centre.ContactEmail, centre.ContactPhone,
            centre.IsActive
        ))
        db.commit()
        centre.CentreID = cursor.lastrowid
    return centre

@app.put("/centres/{centre_id}", response_model=Centre)
def update_centre(centre_id: int, centre: Centre):
    with db.cursor() as cursor:
        sql = """UPDATE centres 
                 SET CentreName=%s, Address=%s, ContactEmail=%s, ContactPhone=%s, IsActive=%s
                 WHERE CentreID=%s"""
        cursor.execute(sql, (
            centre.CentreName, centre.Address,
            centre.ContactEmail, centre.ContactPhone,
            centre.IsActive, centre_id
        ))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Centre not found")
    centre.CentreID = centre_id
    return centre

@app.delete("/centres/{centre_id}")
def delete_centre(centre_id: int):
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM centres WHERE CentreID=%s", (centre_id,))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Centre not found")
    return {"status": "deleted"}


@app.post("/courses", response_model=Course)
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


@app.get("/courses/{course_id}", response_model=Course)
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


@app.get("/courses", response_model=list[Course])
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
    
@app.put("/courses/{course_id}", response_model=Course)
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


# ---- Delete course ----
@app.delete("/courses/{course_id}")
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
    
@app.post("/certificates", response_model=Certificate)
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


@app.get("/certificates/{certificate_id}", response_model=Certificate)
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


@app.get("/certificates", response_model=list[Certificate])
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
    
@app.put("/certificates/{certificate_id}", response_model=Certificate)
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


@app.delete("/certificates/{certificate_id}")
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

    
@app.post("/cohorts", response_model=Cohort)
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


@app.get("/cohorts/{cohort_id}", response_model=Cohort)
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


@app.get("/cohorts", response_model=list[Cohort])
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
    
@app.put("/cohorts/{cohort_id}", response_model=Cohort)
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


@app.delete("/cohorts/{cohort_id}")
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

    
@app.post("/users", response_model=User)
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


@app.get("/users/{user_id}", response_model=User)
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


@app.get("/users", response_model=list[User])
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
    
@app.put("/users/{user_id}", response_model=User)
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


@app.delete("/users/{user_id}")
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

    
@app.post("/courseregistrations", response_model=CourseRegistration)
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


@app.get("/courseregistrations/{registration_id}", response_model=CourseRegistration)
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


@app.get("/courseregistrations", response_model=list[CourseRegistration])
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
    
@app.put("/candidates/{candidate_id}", response_model=Candidate)
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


@app.delete("/candidates/{candidate_id}")
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


@app.get("/issuedcertificates/{issue_id}", response_model=IssuedCertificate)
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


@app.get("/issuedcertificates", response_model=list[IssuedCertificate])
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
    
@app.put("/issuedcertificates/{issue_id}", response_model=IssuedCertificate)
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


@app.delete("/issuedcertificates/{issue_id}")
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
