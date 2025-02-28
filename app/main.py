from fastapi import FastAPI, Request
from app.routes.user_routes import router
from app.database import collection
import time

app = FastAPI(title="User's API", description="API for managing users.") # creating fastAPI app

# To show response time of api calling
@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time']=str(process_time)
    return response

# Include Routers
app.include_router(router=router, tags=['users']) 

@app.get("/")
async def root(): # default root route to check if the server is running
    return {"message": "Welcome to User's API."}

@app.get("/check_document's_count") # route to check the count of documents in the given collection
async def test_db():
    return {'count': collection.count_documents({})}