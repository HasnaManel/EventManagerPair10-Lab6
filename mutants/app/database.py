from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./events.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_get_db__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_get_db__mutmut)
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def x_get_db__mutmut_orig():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def x_get_db__mutmut_1():
    db = None

    try:
        yield db
    finally:
        db.close()

mutants_x_get_db__mutmut['_mutmut_orig'] = x_get_db__mutmut_orig # type: ignore # mutmut generated
mutants_x_get_db__mutmut['x_get_db__mutmut_1'] = x_get_db__mutmut_1 # type: ignore # mutmut generated