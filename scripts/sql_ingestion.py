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

def get_all_prompts_with_usernames():
    """Fetch all prompts with the corresponding username."""
    session = Session()
    try:
        # Query non-admin users and join with prompt logs
        results = (
            session.query(User.username, PromptLog.prompt, PromptLog.response, PromptLog.created_at) \
                .join(PromptLog, User.id == PromptLog.user_id) \
                .filter(User.is_admin == False) \
                .order_by(User.username, PromptLog.created_at) \
                .all()
        )
        if not results:
            print("No prompts found for non-admin users.")
            return []
        print("Prompts with usernames:")
        for username, prompt, response, created_at in results:
            print(f"Username: {username}\nPrompt: {prompt}\nResponse: {response}\nCreated At: {created_at}")
        return results
    except Exception as e:
        print(f"Error fetching prompt data: {e}")
        return []
    finally:
        session.close()

if __name__ == "__main__":
    # ingest_users()
    # admin_prompt()
<<<<<<< Updated upstream
    test_db()
    # print_all_data()
=======
    # test_db()
    # print_all_data()
    get_all_prompts_with_usernames()
>>>>>>> Stashed changes
