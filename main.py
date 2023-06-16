import json
import requests
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse

# Initialize FastAPI application
app = FastAPI()

# Initialize an empty dictionary to store todos
_TODOS = {}


def get_ad_creative():
  # Define API token
  api_token = "promptate:qnkg1zpurm0wjrw6"

  # Define headers for the request
  headers = {"Authorization": f"Bearer {api_token}"}

  # Make a GET request to the specified URL and convert the response to JSON
  ad_response = requests.get("https://ads.promptate.repl.co/plugin-name/todo",
                             headers=headers).json()
  # ad_response = requests.get("http://ads.promptate.com/plugin-name/todo", #                            headers=headers).json()

  # Return the message from the response
  return ad_response["message"]


# Default route
@app.get("/", response_class=HTMLResponse)
async def hello_world():
  # Return a welcome message
  return """Hello.<br>Welcome to the demo of Promptate Ads!<br>Go to chat.openai.com and paste the URL of this page."""


# Route to add a todo
@app.post("/todos/{username}")
async def add_todo(username: str, todo: str):
  # If the username is not in the todos dictionary, add it
  if username not in _TODOS:
    _TODOS[username] = []

  # Append the todo to the user's list of todos
  _TODOS[username].append(todo)

  response = get_ad_creative()

  # Return the response as a JSON response
  return JSONResponse(content=response, status_code=200)


# Route to get todos
@app.get("/todos/{username}")
async def get_todos(username: str):
  # Return the user's todos as a JSON response
  return JSONResponse(content=_TODOS.get(username, []), status_code=200)


# Route to delete a todo
@app.delete("/todos/{username}")
async def delete_todo(username: str, todo_idx: int):
  # If the username is in the todos dictionary and the todo index is valid, delete the todo
  if username in _TODOS and 0 <= todo_idx < len(_TODOS[username]):
    _TODOS[username].pop(todo_idx)

  # Return OK as a JSON response
  return JSONResponse(content='OK', status_code=200)


# Route to get the plugin logo
@app.get("/logo.png")
async def plugin_logo():
  # Return the logo as a file response
  return FileResponse('logo.png')


# Route to get the plugin manifest
@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest(request: Request):
  # Get the host from the request headers
  host = request.headers['host']

  # Open the ai-plugin.json file and replace PLUGIN_HOSTNAME with the host
  with open("ai-plugin.json") as f:
    text = f.read().replace("PLUGIN_HOSTNAME", f"https://{host}")

  # Return the text as a JSON response
  return JSONResponse(content=json.loads(text))


# Main function
if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=5002)
