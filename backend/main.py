from fastapi import FastAPI
from routers import centre, candidate, course, cohort, certificate, user, courseregistration, issuedcertificate, business, auth

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # your React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(centre.router)
app.include_router(candidate.router)
app.include_router(course.router)
app.include_router(cohort.router)
app.include_router(certificate.router)
app.include_router(user.router)
app.include_router(courseregistration.router)
app.include_router(issuedcertificate.router)
app.include_router(business.router)
app.include_router(auth.router)
