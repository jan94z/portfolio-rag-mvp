from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "RAG MVP API is running"}
