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

# get db

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

def delete_users_and_prompts():
    """Delete all users and their associated prompts."""
    session = Session()
    try:
        # Delete all prompt logs first
        session.query(PromptLog).delete()
        # Then delete all users
        session.query(User).delete()
        session.commit()
        print("All users and their prompts have been deleted.")
    except Exception as e:
        print(f"Error deleting users and prompts: {e}")
        session.rollback()
    finally:
        session.close()

    
if __name__ == "__main__":
    ingest_users()
    # admin_prompt()
    # print_all_data()
    test_db()
    # print_all_data()
    # get_all_prompts_with_usernames()
    # delete_users_and_prompts()

