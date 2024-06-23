from pydantic import BaseModel
from config import Config
import openai
import json


# define request query model
class Query(BaseModel):
	content: str


# define template function that builds up a query
def template(context: list[str], question: str):
	user_query = Config.LLM_PROMPT_PREFIX

	for word in context:
		user_query += word + '\n'
	
	user_query += question
	return Config.LLM_PROMPT_SYSTEM, user_query


# prompt an LLM in an asynchronous stream
async def prompt(system_query: str, user_query: str) -> str:
	api_key = Config.OPENAI_KEY

	response = await (openai.AsyncOpenAI(api_key=api_key)).chat.completions.create(
		model="gpt-3.5-turbo-16k",
		messages=[
			{
				'role': 'system',
				'content': system_query
			},
			{
				'role': 'user',
				'content': user_query
			}
		],
		stream=True
	)

	async for chunk in response:
		if chunk.choices[0].delta.content == None:
			yield json.dumps({'response': '', 'done': True}, ensure_ascii=False)
		else:
			yield json.dumps({'response': chunk.choices[0].delta.content, 'done': False}, ensure_ascii=False)
