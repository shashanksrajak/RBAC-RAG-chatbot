from typing import Dict
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from services import chatbot
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
security = HTTPBasic()

# Dummy user database
users_db: Dict[str, Dict[str, str]] = {
    "Tony": {"password": "password123", "role": "engineering"},
    "Bruce": {"password": "securepass", "role": "marketing"},
    "Sam": {"password": "financepass", "role": "finance"},
    "Peter": {"password": "pete123", "role": "engineering"},
    "Sid": {"password": "sidpass123", "role": "marketing"},
    "Natasha": {"password": "hrpass123", "role": "hr"},
    "Shashank": {"password": "password123", "role": "c_level"}

}


# Authentication dependency
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    print(credentials)
    username = credentials.username
    password = credentials.password
    user = users_db.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": username, "role": user["role"]}


# Login endpoint
@app.get("/login")
def login(user=Depends(authenticate)):
    return {"message": f"Welcome {user['username']}!", "role": user["role"]}


# Protected test endpoint
@app.get("/test")
def test(user=Depends(authenticate)):
    return {"message": f"Hello {user['username']}! You can now chat.", "role": user["role"]}


# Protected chat endpoint
@app.post("/chat")
def query(user=Depends(authenticate), message: str = "Hello"):
    answer = chatbot.chatbot_service(user["role"], message)
    return {"user": user, "message": answer, "question": message}


@app.get("/")
def hello():
    return {"message": "Server is running."}


def main():
    print("Hello from chatbot server!")
    uvicorn.run(app, host="0.0.0.0", port=6001)


if __name__ == "__main__":
    main()
