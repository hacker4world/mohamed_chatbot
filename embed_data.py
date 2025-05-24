import os
from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document


os.environ["PINECONE_API_KEY"] = "pcsk_3njQdj_JvBaU7wwJy1L3Gh4g1A9papKGqnzZDdEDqi81ipNDJw78CCNx8Gp5rRSRpxUzAW"

def embed_data():
    with open("data.txt", "r", encoding="utf-8") as f:
        sections = [s.strip() for s in f.read().split("\n\n\n") if s.strip()]
        
        chunks = [
            Document(
                page_content=section,
            )
            for i, section in enumerate(sections)
        ]

        embeddings = OllamaEmbeddings(model="mxbai-embed-large")

        PineconeVectorStore.from_documents(
            documents=chunks,
            embedding=embeddings,
            index_name="kroshu",
            batch_size=100,
        )

        print("Data has been loaded to pinecone")


embed_data()