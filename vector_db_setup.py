from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

def build_vector_db():
    # Read your scraped content
    with open("business_info.txt", "r", encoding="utf-8") as f:
        data = f.read()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(data)

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_texts(chunks, embeddings, persist_directory="db")
    vectordb.persist()
    print("✅ Vector DB created and saved in ./db")

if __name__ == "__main__":
    build_vector_db()
