
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
from dotenv import load_dotenv
app = FastAPI()

from actions import crawl_and_extract_llms_elements, elements_to_llms_txt

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv("common.env")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

@app.get('/auth/pipedrive/callback')
async def pipedrive_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Missing code"}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://oauth.pipedrive.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        token_data = response.json()
    
    # Optionally, you can redirect the user or return a success message
    if response.status_code == 200:
        return {"success": token_data}
    else:
        return {"error": "Failed to retrieve access token", "details": token_data}


@app.post("/api/llms-txt")
async def create_llms_txt(request: Request):
    data = await request.json()
    print(data)
    url = data.get("url")

    
    elements = crawl_and_extract_llms_elements(url) 
    llms_txt = elements_to_llms_txt(elements)
    return {"llms_txt": llms_txt}

# WIP handler = Mangum(app)  # <-- Required for AWS Lambda!


if __name__ == "__main__":
    import uvicorn
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host=host, port=port)