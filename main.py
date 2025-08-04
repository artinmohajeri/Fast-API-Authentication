
from fastapi import FastAPI, Form, Header, HTTPException
import sqlite3
from passlib.hash import bcrypt

app = FastAPI()  # Create the FastAPI app
API_KEY = "secret123"

@app.post("/signup")
def signup(
    username: str = Form(None),
    password: str = Form(None),
    x_api_key: str = Header(None, alias="X-API-Key")
):

    if not x_api_key:
        raise HTTPException(status_code=401, detail="Don't mess with us.")

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Don't mess with us.")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Bad request")

    hashed_password = bcrypt.hash(password)
    print(hashed_password)

    # Check if user exists
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=400, detail=f"username: {username} already exists")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password)
    )
    conn.commit()
    conn.close()

    return {
        "message": f"User {username} added to the database ✅",
    }



def get_user(username: str):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()  # Returns (username, password) or None
    conn.close()
    return user

@app.post("/login")
def login(
    username: str = Form(None),
    password: str = Form(None),
    x_api_key: str = Header(None, alias="X-API-Key")
):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Don't mess with us.")

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Don't mess with us.")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Bad request")
    
    
    user = get_user(username=username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    stored_password = user[1]  # user[0] is username, user[1] is password
    is_valid = bcrypt.verify(password, stored_password)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Wrong password")

    return {"message": "Login successful! ✅"}


@app.get("/get-all-users")
def get_all_users():
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        # Fetch all users (only username shown for security)
        cursor.execute("SELECT username FROM users")
        users = cursor.fetchall()  # Returns list of tuples like [('user1',), ('user2',)]
        
        conn.close()
        
        # Convert to simple list of usernames
        return {"users": [user[0] for user in users]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))