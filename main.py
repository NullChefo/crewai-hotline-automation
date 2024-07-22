from fastapi import FastAPI, Form

app = FastAPI(
    title="AI Hotline Automation API",
    description="The hotline automation API.",
    version="0.0.1",
    # terms_of_service="http://example.com/terms/",
    # contact={
    #     "name": "API Support",
    #     "url": "http://example.com/contact/",
    #     "email": "support@example.com",
    # },
    # license_info={
    #     "name": "Apache 2.0",
    #     "url": "http://www.apache.org/licenses/LICENSE-2.0.html",
    # },
    # openapi_url="/api/v1/openapi.json",
    # docs_url="/api/v1/docs",
    # redoc_url="/api/v1/redoc",
)


@app.get("/health")
def read_health():
    return {"message": "Healthy"}


@app.post("/caller_automation")
async def caller_automation(caller_id: str = Form(...)):
    return {"caller_id": caller_id}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
