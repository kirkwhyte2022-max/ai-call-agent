from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import openai, gtts, os

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

# Load your vector database
embeddings = OpenAIEmbeddings()
vectordb = Chroma(persist_directory="db", embedding_function=embeddings)

@app.route("/voice", methods=["POST"])
def voice():
    user_text = request.values.get("SpeechResult", "Hello?")

    # Search for relevant chunks from your website
    docs = vectordb.similarity_search(user_text, k=3)
    context = "\n".join([d.page_content for d in docs])

    # Ask GPT for a response
    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are a friendly and professional receptionist for Caribbean Orthopaedic Centre. Use this context to answer accurately:\n{context}"},
            {"role": "user", "content": user_text}
        ]
    )

    reply = completion.choices[0].message["content"]
    print(f"User: {user_text}\nAI: {reply}")

    # Convert text to speech
    tts = gtts.gTTS(reply)
    tts.save("reply.mp3")

    response = VoiceResponse()
    response.play("https://YOUR-RENDER-APP-URL/reply.mp3")

    # Log the conversation
    with open("call_log.txt", "a", encoding="utf-8") as f:
        f.write(f"User: {user_text}\nAI: {reply}\n---\n")

    return Response(str(response), mimetype="text/xml")

@app.route("/reply.mp3")
def serve_reply():
    return Response(open("reply.mp3", "rb"), mimetype="audio/mpeg")

@app.route("/")
def home():
    return "AI Call Agent running successfully!"

if __name__ == "__main__":
    app.run(port=5000)
