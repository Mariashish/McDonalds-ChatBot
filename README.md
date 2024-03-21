# McDonald's Chatbot
This repository contains the source code for a McDonald's chatbot implemented using FastAPI and the OpenAI API. The chatbot is designed to handle conversations with users and provide generic responses to questions about McDonald's.

## Prerequisites
Make sure you have the following Python packages installed:

fastapi
openai
pydantic
uvicorn
You can install them by running the following command:

### bash
pip install fastapi openai pydantic uvicorn

## Configuration
Before running the chatbot, you need to configure the following environment variables:

OPENAI_API_KEY: API key for accessing the OpenAI API.
ASSISTANT_ID: ID of the OpenAI assistant to use for responses.
Ensure you set these environment variables in your runtime environment.

## Usage
The chatbot provides two endpoints for interaction:

Start Conversation (/start): This endpoint initiates a new conversation with the chatbot and returns a unique conversation ID (thread_id). You need to call this endpoint before sending messages to the chatbot.

Chat (/chat): This endpoint handles messages sent by the user to the chatbot. It requires the conversation ID (thread_id) and the message sent by the user. The chatbot will process the message and provide an appropriate response.
