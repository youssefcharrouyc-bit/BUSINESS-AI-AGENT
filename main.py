

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from api.middleware import RateLimitMiddleware
from api.router import router

load_dotenv()

app = FastAPI(title="Business AI Agent", version='1.0.0')


# Include router
app.include_router(router)

app.add_middleware(RateLimitMiddleware, requests_per_minute=2)

# Mount UI
app.mount("/app", StaticFiles(directory="UI", html=True), name="UI" )



@app.get("/")
async def root():
    return RedirectResponse(url="/app")


if __name__ == "__main__":
    print("Starting AI Agent Server...")
    print("Open url in your browser")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    