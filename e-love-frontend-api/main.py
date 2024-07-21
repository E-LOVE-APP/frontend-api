from fastapi import FastAPI

app = FastAPI()

# @app.on_event("startup")
# async def startup_event():
#     print(f"Database URL: {settings.DATABASE_URL}")
#     print(f"Secret Key: {settings.SECRET_KEY}")

@app.get("/hello")
async def hello():
    return {"message": "Hello, World!"}