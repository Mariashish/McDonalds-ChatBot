import os
from time import sleep
from packaging import version
import openai
from openai import OpenAI
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import asyncio

# Controlliamo che la versione di OpenAI sia corretta
required_version = version.parse("1.1.1")
current_version = version.parse(openai.__version__)
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
if current_version < required_version:
  raise ValueError(f"Error: OpenAI version {openai.__version__}"
                   " is less than the required version 1.1.1")
else:
  print("OpenAI version is compatible.")

# Inizializziamo l'app FastAPI
app = FastAPI()

# Inizializziamo il client di OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Carichiamo l'ID dell'assistente dalle variabili di ambiente
assistant_id = os.environ['ASSISTANT_ID']

# Definiamo il modello di richiesta per la chat
class ChatRequest(BaseModel):
    thread_id: str
    message: str

# Inizializziamo una conversazione
@app.get('/start')
async def start_conversation():
  print("Starting a new conversation...")
  thread = client.beta.threads.create()
  print(f"New thread created with ID: {thread.id}")
  return {"thread_id": thread.id}

# Gestiamo il messaggio di chat
@app.post('/chat')
async def chat(chat_request: ChatRequest):
  thread_id = chat_request.thread_id
  user_input = chat_request.message

  # Controlliamo che l'ID della conversazione sia stato fornito
  if not thread_id:
    print("Error: Missing thread_id")
    raise HTTPException(status_code=400, detail="Missing thread_id")

  print(f"Received message: {user_input} for thread ID: {thread_id}")

  # Inseriamo il messaggio dell'utente nella conversazione
  client.beta.threads.messages.create(thread_id=thread_id,
                                      role="user",
                                      content=user_input)

  # Creiamo la run per l'assistente
  run = client.beta.threads.runs.create(thread_id=thread_id,
                                        assistant_id=assistant_id)
  
  end = False

  # Polling per controllare lo stato della run 
  while not end:
    # Controlliamo lo stato della run
    run_status = client.beta.threads.runs.retrieve(thread_id=thread_id,
                                                   run_id=run.id)
    print(f"Run status: {run_status.status}")

    if run_status.status == 'completed':
      end = True
     
    elif run_status.status == "cancelling" or run_status.status == "requires_action" or run_status.status == "cancelled" or run_status.status == "expired":
      end = True

    elif run_status.status == "failed":
      print(run.last_error)
      end = True
    
    await asyncio.sleep(1)  

  # Recuperiamo i messaggi della conversazione
  messages = client.beta.threads.messages.list(thread_id=thread_id)
  # Recuperiamo il testo della risposta
  response = messages.data[0].content[0].text.value
  
  print(f"Assistant response: {response}")

  return {"response": response}
