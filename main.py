from database import Mongo
from data import mongo_client
import uvicorn
import parser
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app.dbase = Mongo(client=mongo_client, collection_name='Sites')

@app.on_event("shutdown")
async def shutdown_db_client():
    app.dbase.mongodb_client.close()

@app.post("/parse")
async def parse_links(req_body: dict):
    links = req_body.get('links')
    if not links:
        return {"error": "links must be a body"}
    if len(links) > 50:
        return {"error": "Max links = 50"}
    response = {}
    for link in links:
        is_insert = await app.dbase.find_key(key=link)
        if not is_insert:
            site = parser.parse_link(link=link)
            if site.get('result') is True:
                await app.dbase.add_site(site)
                response[link] = site.get('html')
            else:
                response[link] = "error parsing"
        else:
            response[link] = is_insert.get('html')
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)



