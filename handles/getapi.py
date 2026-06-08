import aiohttp
async def get_info():
    url=f"http://127.0.0.1:8000/app/sellcars"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status== 404: 
             return None
            data=await resp.json()
            return data