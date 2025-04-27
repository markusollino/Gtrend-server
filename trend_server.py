from fastapi import FastAPI
from pydantic import BaseModel
from pytrends.request import TrendReq

# Create a FastAPI app
app = FastAPI()

# Define what data the server expects
class KeywordRequest(BaseModel):
    keyword: str

# Define a route that handles incoming requests
@app.post("/get_trends")
def get_trends(request: KeywordRequest):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([request.keyword], cat=0, timeframe='today 3-m', geo='', gprop='')
    data = pytrends.interest_over_time()
    
    if not data.empty:
        # Return the trends data as a dictionary
        return data[request.keyword].to_dict()
    else:
        return {"error": "No data found for that keyword"}
