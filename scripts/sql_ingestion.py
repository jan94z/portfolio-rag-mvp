from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from backend.core.sql import User, PromptLog, Base
import os

# Load environment variables
load_dotenv("/home/jan/portfolio-rag-mvp/.env")
DATABASE_URL = f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('DROPLET_IP')}:5432/{os.environ.get('POSTGRES_DB')}"
USERLIST = os.environ.get("USERS")
PROMPT_LIMIT = int(os.environ.get("PROMPT_LIMIT", 10))
ADMIN_USERS = set(name.strip() for name in os.environ.get("ADMIN", "").split(","))

# --- Database setup ---
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def ingest_users():
    session = Session()
    for user_entry in USERLIST.split(","):
        username, password = user_entry.strip().split(":")
        # Check if user already exists
        if not session.query(User).filter_by(username=username).first():
            if username in ADMIN_USERS:
                user = User(
                username=username,
                prompt_limit=10000,
                is_admin=True
            )
            else:
                user = User(
                    username=username,
                    prompt_limit=PROMPT_LIMIT
                )
            user.password = password
            session.add(user)
    session.commit()
    session.close()
    print("Users successfully ingested.")

# def admin_prompt():
#     # make a dummy prompt log for each admin user so that the db is not empty
#     session = Session()
#     for admin in ADMIN_USERS:
#         user = session.query(User).filter_by(username=admin).first()
#         if user:
#             prompt_log = PromptLog(
#                 user_id=user.id,
#                 prompt="This is a dummy prompt.",
#                 response="This is a dummy response."
#             )
#             session.add(prompt_log)
#     session.commit()
#     session.close()
#     print("Admin prompt logs successfully ingested.")

def test_db():
    """Test the database connection and basic operations."""
    session = Session()
    try:
        # Test if we can query the User table
        users = session.query(User).all()
        prompts = session.query(PromptLog).all()
        print(f"Found {len(users)} users in the database.")
        print(users)
        print(f"Found {len(prompts)} prompt logs in the database.")
        print(prompts)
    except Exception as e:
        print(f"Database test failed: {e}")
    finally:
        session.close()

def print_all_data():
    """Print all users and prompt logs."""
    session = Session()
    try:
        users = session.query(User).all()
        prompts = session.query(PromptLog).all()
        print("Users:")
        for user in users:
            print(f"Username: {user.username}, Prompt Limit: {user.prompt_limit}, Prompt Count: {user.prompt_count}, Is Admin: {user.is_admin}")
        print("\nPrompt Logs:")
        for prompt in prompts:
            print(f"User ID: {prompt.user_id}, Prompt: {prompt.prompt}, Response: {prompt.response}")
    except Exception as e:
        print(f"Error fetching data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    ingest_users()
    # admin_prompt()
    test_db()
    # print_all_data()
