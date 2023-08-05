import uvicorn

def main():
    uvicorn.run("server:app", port=5000, reload=True, reload_dirs=[".."], workers=1)
