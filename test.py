from fastapi import FastAPI

app = FastAPI()
@app.get("/food-items")
async def get_good_items():
    return {"status":"success", "data": ["Pizza", "Burger", "Sushi"]}