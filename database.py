import motor.motor_asyncio

class Mongo:
    def __init__(self, client, collection_name, uri="mongodb://localhost:27017"):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client[client]
        self.collection = self.db[collection_name]

    async def find_key(self, key):
        document = await self.collection.find_one({"link": key})
        return document

    async def add_site(self, site):
        link = site.get('link')
        html = site.get('html')
        if link and html:
            document = {
                    "link": link,
                    "html": html
                }
            result = await self.collection.insert_one(document=document)
            return result

    async def get_sites(self):
        sites = self.collection.find({})
        return sites

    async def remove_site(self, key, value):
        result = self.collection.delete_many({key: value})
        return result
