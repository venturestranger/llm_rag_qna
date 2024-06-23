from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from vdb import VDB
from utils import Query, template, prompt
from config import Config
import uvicorn


# initialize app and API versioning
app = FastAPI()
api_v1 = FastAPI()
vdb = VDB()


# declare API V1 handlers
@api_v1.post('/fetch')
async def fetch_v1(query: Query):
	fetched = vdb.fetch(query.content)
	system_query, user_query = template(fetched, query.content)

	return StreamingResponse(prompt(system_query, user_query), media_type='application/json')


# ensuring CORS policy supported
app.add_middleware(
	CORSMiddleware,
	allow_origins=['*'],
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*']
)


# mount APIs
app.mount('/ai/api/rest/v1/', api_v1)


# program entry points
if __name__ == '__main__':
	import uvicorn 

	uvicorn.run(app, host=Config.HOST, port=Config.PORT)

def factory_app():
	return app
