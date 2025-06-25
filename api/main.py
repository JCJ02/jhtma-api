from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.utilities.app_response import AppResponse
from api.configurations.configuration import configuration
from api.routes import router as api_router

# INITIALIZE FastAPI APP
app = FastAPI(
    title = "Job Hunting Tracker Mobile App API Documentation",
    description = "The Job Hunting Tracker Mobile App empowers you to keep every application organized and accounted for. From the moment you hit 'submit' to that final decision, you'll have a clear overview. Log company names, roles, and application dates, then simply update the status as you move through the hiring process - whether it's pending a response, an interview, an acceptance, or a rejection. Simplify your job hunt and stay on top of your game.",
    version = "1.0.0",
)

# MIDDLEWARE FOR CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REGISTERED ENDPOINTS
app.include_router(api_router)

# ROOT ENDPOINT
@app.get("/", tags=["Root"])
async def root():   
    return AppResponse.send_successful(
        data = None,
        message = "Job Hunting Tracker Mobile Application!",
        code = 200
    )

# # RUN THE SERVER
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.main:app",
        port = int(configuration["app"]["port"]),
        reload = True,
    )