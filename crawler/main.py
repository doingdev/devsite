import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
# from mangum import Mangum

from actions import crawl_and_extract_llms_elements, elements_to_llms_txt

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/llms-txt")
async def create_llms_txt(request: Request):
    data = await request.json()
    print(data)
    url = data.get("url")

    
    elements = crawl_and_extract_llms_elements(url) 
    llms_txt = elements_to_llms_txt(elements)
    return {"llms_txt": llms_txt}

# handler = Mangum(app)  # <-- Required for AWS Lambda!


if __name__ == "__main__":
    import uvicorn
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host=host, port=port)