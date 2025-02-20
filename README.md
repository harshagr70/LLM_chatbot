# LLM powered chatbot

This is a full-stack web application integrating **FastAPI** as the backend and a **React** frontend, with **Neo4j** as the database . 

Ensure you have the following installed before proceeding:  

- **Python 3.8+**  
- **FastAPI** (Backend framework)  
- **Node.js 16+** (For frontend)  
- **Neo4j** (Graph database)  
- **Docker** (Optional, for Neo4j)  
- **Git** (For version control)  

---

## 🛠️ Backend Setup  

## Clone the Repository  
```sh
git clone <your-repository-url>
cd <your-project-folder>/backend

## create new virtual enviroment 

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

#install dependencies 

pip install -r requirements.txt

#configure enviroment variables

NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=yourpassword
ALLOWED_ORIGIN=http://localhost:5173

##intsall Ollama locally 
https://ollama.com/download/mac

## run Ollama instance 

ollama run llama 3.2 

## neo4j sample data setup 

run the script from - /backend/neo4j_query.txt  to generate the sample data 

## run the backend server  (note - make sure neo4j instance is live and running )

python backend.py 

api end point will be now available at - http://localhost:8000



##FRONT_END setup 

##navigate to Frontend folder

cd ../frontend

##install dependencies 

npm install 

## start the frontend server 

npm run dev 

## Interface @ 
http://localhost:5173


## **note  (!! important )

> **Note:** This bot is designed to generate Cypher queries based on the predefined database schema. For best results, ask questions relevant to the provided schema. If the schema changes, the bot must be retrained with new examples to maintain accuracy.
