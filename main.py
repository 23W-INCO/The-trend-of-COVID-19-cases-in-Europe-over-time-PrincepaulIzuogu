from fastapi import FastAPI
from fastapi.responses import FileResponse
from visualization import construct_choropleth  # Import the function
import os
import json
import uvicorn

app = FastAPI()

# Get the path to the current file directory
dir_path = os.path.dirname(os.path.realpath(__file__))

@app.get("/", response_class=FileResponse)
async def index():
    return FileResponse(os.path.join(dir_path, "templates/index.html"))

@app.get("/get-choropleth-data")
async def get_choropleth_data():
    choropleth_data = construct_choropleth()
    return choropleth_data

@app.get("/aboutus", response_class=FileResponse)
async def aboutus():
    return FileResponse(os.path.join(dir_path, "templates/aboutus.html"))

@app.get("/aboutapp", response_class=FileResponse)
async def aboutapp():
    return FileResponse(os.path.join(dir_path, "templates/aboutapp.html"))

@app.get("/static/{file_path:path}")
async def serve_static(file_path: str):
    static_file_path = os.path.join(dir_path, "static", file_path)
    if os.path.exists(static_file_path):
        return FileResponse(static_file_path)

@app.get("/get-search-data")
async def get_search_data(location: str = Query(None), date: str = Query(None)):
    # Read data from data.json based on provided location and date
    with open(os.path.join(dir_path, "data.json")) as json_file:
        data = json.load(json_file)
        search_result = [item for item in data if item["location"] == location and item["date"] == date]
    return search_result

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=5000)
