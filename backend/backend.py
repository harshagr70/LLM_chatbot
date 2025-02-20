from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from neo4j import GraphDatabase
from neo4j_graphrag.retrievers import Text2CypherRetriever
from neo4j_graphrag.generation import GraphRAG
from langchain_community.llms import Ollama
from dotenv import load_dotenv
import os


load_dotenv()
# ------------------------------------------------------------------------------
class LLMResponse:
    def __init__(self, content: str):
        self.content = content

# ------------------------------------------------------------------------------
class LocalLlamaLLM:
    def __init__(self, model="llama3", temperature=0):
        self.llm = Ollama(model=model)
        self.temperature = temperature

    def __call__(self, prompt: str, *args, **kwargs) -> LLMResponse:
        return self.invoke(prompt, *args, **kwargs)

    def invoke(self, prompt: str, *args, **kwargs) -> LLMResponse:
        response_text = self.llm.invoke(prompt, *args, **kwargs)
        return LLMResponse(response_text)

    def predict(self, prompt: str, *args, **kwargs) -> LLMResponse:
        return self.__call__(prompt, *args, **kwargs)

# ------------------------------------------------------------------------------

def get_env_var(var_name: str):
    """Retrieve an environment variable and raise an error if it is missing."""
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Missing required environment variable: {var_name}")
    return value

URI = get_env_var("NEO4J_URI")
USER = get_env_var("NEO4J_USER")
PASSWORD = get_env_var("NEO4J_PASSWORD")
AUTH = (USER, PASSWORD)

# Establish connection to the Neo4j database.
driver = GraphDatabase.driver(URI, auth=AUTH)

# ------------------------------------------------------------------------------
neo4j_schema = """
Node properties:
Movie {title: STRING, released: INTEGER, genre: STRING}
Actor {name: STRING}
Director {name: STRING}

Relationships:
(:Actor)-[:ACTED_IN]->(:Movie)
(:Director)-[:DIRECTED]->(:Movie)
"""

# ------------------------------------------------------------------------------
examples = [
    "USER INPUT: 'Which actors starred in the Matrix?' QUERY: MATCH (p:Person)-[:ACTED_IN]->(m:Movie) WHERE m.title = 'The Matrix' RETURN p.name"
    "USER INPUT: 'Which actors starred in The Matrix?' QUERY: MATCH (p:Actor)-[:ACTED_IN]->(m:Movie) WHERE m.title = 'The Matrix' RETURN p.name"  
    "USER INPUT: 'Who directed Inception?' QUERY: MATCH (d:Director)-[:DIRECTED]->(m:Movie) WHERE m.title = 'Inception' RETURN d.name"  
    "USER INPUT: 'List all movies directed by Christopher Nolan.' QUERY: MATCH (d:Director {name: 'Christopher Nolan'})-[:DIRECTED]->(m:Movie) RETURN m.title"  
    "USER INPUT: 'Which movies did Leonardo DiCaprio act in?' QUERY: MATCH (a:Actor {name: 'Leonardo DiCaprio'})-[:ACTED_IN]->(m:Movie) RETURN m.title"  
    "USER INPUT: 'List all action movies.' QUERY: MATCH (m:Movie) WHERE m.genre = 'Action' RETURN m.title"  
    "USER INPUT: 'Find all sci-fi movies.' QUERY: MATCH (m:Movie) WHERE m.genre = 'Sci-Fi' RETURN m.title"  
    "USER INPUT: 'Who acted in The Dark Knight?' QUERY: MATCH (a:Actor)-[:ACTED_IN]->(m:Movie) WHERE m.title = 'The Dark Knight' RETURN a.name"  
    "USER INPUT: 'Which movies were released in 2010?' QUERY: MATCH (m:Movie) WHERE m.released = 2010 RETURN m.title"  
    "USER INPUT: 'Who directed The Matrix?' QUERY: MATCH (d:Director)-[:DIRECTED]->(m:Movie) WHERE m.title = 'The Matrix' RETURN d.name"  
    "USER INPUT: 'Find all movies Keanu Reeves acted in.' QUERY: MATCH (a:Actor {name: 'Keanu Reeves'})-[:ACTED_IN]->(m:Movie) RETURN m.title"  
    "USER INPUT: 'List all directors.' QUERY: MATCH (d:Director) RETURN d.name"  
    "USER INPUT: 'List all actors.' QUERY: MATCH (a:Actor) RETURN a.name"  
    "USER INPUT: 'Find all movies released after 2000.' QUERY: MATCH (m:Movie) WHERE m.released > 2000 RETURN m.title"  
    "USER INPUT: 'List all movies released before 2010.' QUERY: MATCH (m:Movie) WHERE m.released < 2010 RETURN m.title"  
    "USER INPUT: 'Who directed Interstellar?' QUERY: MATCH (d:Director)-[:DIRECTED]->(m:Movie) WHERE m.title = 'Interstellar' RETURN d.name"  
    "USER INPUT: 'Which actors have acted in both The Matrix and The Matrix Reloaded?' QUERY: MATCH (a:Actor)-[:ACTED_IN]->(m1:Movie {title: 'The Matrix'}), (a)-[:ACTED_IN]->(m2:Movie {title: 'The Matrix Reloaded'}) RETURN a.name"  
    "USER INPUT: 'Find movies that Christian Bale has acted in.' QUERY: MATCH (a:Actor {name: 'Christian Bale'})-[:ACTED_IN]->(m:Movie) RETURN m.title"  
    "USER INPUT: 'Who produced The Dark Knight?' QUERY: MATCH (p:Person)-[:PRODUCED]->(m:Movie) WHERE m.title = 'The Dark Knight' RETURN p.name"  
    "USER INPUT: 'Find movies that were both directed and produced by Christopher Nolan.' QUERY: MATCH (d:Director {name: 'Christopher Nolan'})-[:DIRECTED]->(m:Movie)<-[:PRODUCED]-(d) RETURN m.title"  
    "USER INPUT: 'List all movies along with their release year.' QUERY: MATCH (m:Movie) RETURN m.title, m.released"  

]

# ------------------------------------------------------------------------------
local_llm_for_retriever = LocalLlamaLLM(model="llama3.2")
retriever = Text2CypherRetriever(driver=driver, llm=local_llm_for_retriever, neo4j_schema=neo4j_schema, examples=examples)
local_llm_for_generation = LocalLlamaLLM(model="llama3.2")
rag = GraphRAG(retriever=retriever, llm=local_llm_for_generation)

# ------------------------------------------------------------------------------
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow only your frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def get_answer(request: QueryRequest):
    try:
        query_text = request.query
        search_results = retriever.search(query_text=query_text)
        generated_cypher = search_results.metadata.get("generated_cypher", "No Cypher query generated")

        response = rag.search(query_text=query_text)
        final_answer = response.answer

        return {
            "final_answer": final_answer
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
