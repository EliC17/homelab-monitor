import asyncio, requests
from scheduler import run
 
def fetch_targets():
    return requests.get("http://localhost:8000/api/v1/targets").json()
 
if __name__ == "__main__":
    targets = [t for t in fetch_targets() if t["enabled"]]
    asyncio.run(run(targets))
