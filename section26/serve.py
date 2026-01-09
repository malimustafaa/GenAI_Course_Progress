from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langserve import add_routes
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
model = ChatGroq(model="llama-3.1-8b-instant",groq_api_key=groq_api_key)

generic_template = "Translate the following into {language}:"
prompt = ChatPromptTemplate.from_messages(
    [
        ("system",generic_template),("human","{text}")
    ]
)
parser = StrOutputParser()
#create chain
chain = prompt|model|parser

#app definition
app = FastAPI(title="Langchain Server",
version="1.0",
description="A simple API server using langchain runnable")

#adding chain routes
add_routes(
    app,
    chain,
    path='/chain'
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)


    

"""
LangServe automatically creates the API for you.

Now the clear explanation 👇

What is happening in your code?

You did NOT manually write any FastAPI endpoints like:

@app.post("/translate")
def translate(...):


Yet you still see APIs in localhost:8000/docs.

Why?

Because this line:

add_routes(app, chain, path="/chain")


👉 Auto-generates FastAPI endpoints for your LangChain Runnable.

What APIs does LangServe create?

When you open /docs, LangServe creates:

1️⃣ /chain/invoke

Input: { "language": "...", "text": "..." }

Output: translated text

2️⃣ /chain/batch

Run multiple inputs at once

3️⃣ /chain/stream

Streaming responses (token by token)

4️⃣ /chain/input_schema

Auto-generated input schema (from your prompt variables)

5️⃣ /chain/output_schema

Output schema (from StrOutputParser)

Why do you see input_schema and output_schema?

LangServe introspects your chain:

prompt → model → StrOutputParser


From this it learns:

Inputs required → {language, text}

Output type → str

So FastAPI auto-documents it using OpenAPI.

"""