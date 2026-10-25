from fastapi import FastAPI

from .database import Base, engine
from .routers import events, participants, registrations


app = FastAPI(
    title="Event Manager API",
    description="A teaching project for Git, Docker and CI/CD",
    version="1.0.0"
)


Base.metadata.create_all(bind=engine)


app.include_router(events.router)
app.include_router(participants.router)
app.include_router(registrations.router)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict

@app.get("/")
def root():
    return {
        "message": "Welcome to Event Manager API"
    }