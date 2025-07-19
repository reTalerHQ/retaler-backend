from fastapi import FastAPI
from routes.v1.user import router as user_router
from database.database import Base, engine
from middleware.middleware import add_process_time_header

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI( title="Retaler API",
                description="A RESTful API for managing users in a retail application",
                version="1.0.0",
                contact={
                    "name": "Retaler Support",
                    "email": "retaler@mail.com",
                    "url": "https://retaler.com/support"
                })

app.middleware("http")(add_process_time_header)
app.include_router(user_router, prefix="/v1/users", tags=["users"])
@app.get("/")
async def read_root():
    return {"message": "Welcome to retaler"}
