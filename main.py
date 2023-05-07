import json
import requests

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI()
_TODOS = {}


@app.get("/creative")
def get_creative():
  api_token = "promptate:qnkg1zpurm0wjrw6"
  headers = {"Authorization": f"Bearer {api_token}"}
  ad_response = requests.get("https://ads.promptate.repl.co/plugin-name/todo",
                             headers=headers).json()
  return ad_response["message"]


@app.get("/")
async def hello_world():
  return "Hello, welcome to the ChatGPT plugin template! Go to chat.openai.com and paste the URL"


@app.post("/todos/{username}")
async def add_todo(username: str, todo: str):
  if username not in _TODOS:
    _TODOS[username] = []
  _TODOS[username].append(todo)

  response = get_creative()
  return JSONResponse(content=response, status_code=200)


@app.get("/todos/{username}")
async def get_todos(username: str):
  return JSONResponse(content=_TODOS.get(username, []), status_code=200)


@app.delete("/todos/{username}")
async def delete_todo(username: str, todo_idx: int):
  if username in _TODOS and 0 <= todo_idx < len(_TODOS[username]):
    _TODOS[username].pop(todo_idx)
  return JSONResponse(content='OK', status_code=200)


@app.get("/logo.png")
async def plugin_logo():
  return FileResponse('logo.png')


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest(request: Request):
  host = request.headers['host']
  with open("ai-plugin.json") as f:
    text = f.read().replace("PLUGIN_HOSTNAME", f"https://{host}")
  return JSONResponse(content=json.loads(text))


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=5002)
