from sqlalchemy.orm import Session, declarative_base, relationship, Session, sessionmaker
from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, Text, create_engine, DateTime, func
)
from sqlalchemy.ext.hybrid import hybrid_property
import bcrypt
from typing import Optional
import os

Base = declarative_base()
engine = create_engine(f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@postgres:5432/{os.environ.get('POSTGRES_DB')}")
SessionLocal = sessionmaker(bind=engine)

# --- MODELS ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    _password_hash = Column("password_hash", String, nullable=False)
    prompt_count = Column(Integer, default=0)
    prompt_limit = Column(Integer, default=10)
    is_admin = Column(Boolean, default=False)

    prompts = relationship("PromptLog", back_populates="user")

    @hybrid_property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, plaintext):
        self._password_hash = bcrypt.hashpw(plaintext.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, plaintext):
        return bcrypt.checkpw(plaintext.encode(), self._password_hash.encode())

class PromptLog(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="prompts")

# --- API FUNCTIONS ---
def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Fetch a user by username."""
    return db.query(User).filter(User.username == username).first()

def verify_user_password(db: Session, username: str, password: str) -> bool:
    """Verify user's password."""
    user = get_user_by_username(db, username)
    if user and user.verify_password(password):
        return True
    return False

def is_admin_user(db: Session, username: str) -> bool:
    """Check if a user has admin privileges."""
    user = get_user_by_username(db, username)
    return user.is_admin if user else False

def increment_prompt_count(db: Session, username: str) -> bool:
    """
    Increment the user's prompt count.
    Returns True if prompt is allowed, False if prompt limit exceeded.
    """
    user = get_user_by_username(db, username)
    if not user:
        return False
    if user.prompt_count < user.prompt_limit:
        user.prompt_count += 1
        db.commit()
        return True
    return False

def log_prompt(db: Session, username: str, prompt: str, response: str):
    """Save the user's prompt and the AI response."""
    user = get_user_by_username(db, username)
    if user:
        log = PromptLog(user_id=user.id, prompt=prompt, response=response)
        db.add(log)
        db.commit()
