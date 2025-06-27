import pandas as pd
from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database']  # Replace 'your_database' with your database name

# Define collections for each entity
aluno_collection = db['aluno']
escola_collection = db['escola']
osc_collection = db['osc']
turma_collection = db['turma']

# Function to process the date fields and convert them to datetime objects
def process_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return None

# Function to process a CSV and insert data into MongoDB
def populate_collection(csv_path, collection, schema_mapping):
    # Read the CSV into a pandas dataframe
    df = pd.read_csv(csv_path, delimiter=";", encoding="utf-8-sig")
    
    # Iterate over each row and map the data to the MongoDB schema
    for _, row in df.iterrows():
        document = {}
        
        # Map each column in the CSV to the document structure defined by the schema
        for field, mongo_field in schema_mapping.items():
            value = row.get(field)
            
            # If the field should be a date, process it
            if mongo_field.get('bsonType') == 'date':
                value = process_date(value)
            
            document[mongo_field['name']] = value
        
        # Insert the document into MongoDB
        collection.insert_one(document)

# Define schema mappings for each collection
aluno_schema = {
    "nascimento": {"name": "nascimento", "bsonType": "date"},
    "situacao": {"name": "situacao", "bsonType": "array"},
    "racaCor": {"name": "racaCor", "bsonType": "string"},
    "paisNasc": {"name": "paisNasc", "bsonType": "string"},
    "cadastro": {"name": "cadastro", "bsonType": "long"},
    "sexo": {"name": "sexo", "bsonType": "string"},
    "turma": {"name": "turma", "bsonType": "object"},
    "nee": {"name": "nee", "bsonType": "string"}
}

escola_schema = {
    "rede": {"name": "rede", "bsonType": "string"},
    "nomeDistrito": {"name": "nomeDistrito", "bsonType": "string"},
    "dre": {"name": "dre", "bsonType": "string"},
    "ambientes": {"name": "ambientes", "bsonType": "array"},
    "nomeEsc": {"name": "nomeEsc", "bsonType": "string"},
    "tipoEsc": {"name": "tipoEsc", "bsonType": "string"},
    "parceria": {"name": "parceria", "bsonType": "object"},
    "codInep": {"name": "codInep", "bsonType": "long"},
    "subpref": {"name": "subpref", "bsonType": "string"}
}

osc_schema = {
    "parcerias": {"name": "parcerias", "bsonType": "array"},
    "nome": {"name": "nome", "bsonType": "string"},
    "_id": {"name": "_id", "bsonType": "objectId"},
    "cnpj": {"name": "cnpj", "bsonType": "string"}
}

turma_schema = {
    "etapaEnsino": {"name": "etapaEnsino", "bsonType": "string"},
    "vagas": {"name": "vagas", "bsonType": "int"},
    "serie": {"name": "serie", "bsonType": "object"},
    "tipoTurma": {"name": "tipoTurma", "bsonType": "string"},
    "nomeEsc": {"name": "nomeEsc", "bsonType": "string"},
    "_id": {"name": "_id", "bsonType": "objectId"},
    "turno": {"name": "turno", "bsonType": "object"},
    "matriculados": {"name": "matriculados", "bsonType": "int"},
    "cicloEnsino": {"name": "cicloEnsino", "bsonType": "string"},
    "nomeTurma": {"name": "nomeTurma", "bsonType": "string"}
}

# Populate each collection
populate_collection('datasets/matriculas.csv', aluno_collection, aluno_schema)
populate_collection('datasets/turmas.csv', turma_collection, turma_schema)
populate_collection('datasets/parcerias.csv', osc_collection, osc_schema)
populate_collection('datasets/escolas.csv', escola_collection, escola_schema)

# Close MongoDB connection
client.close()

print("MongoDB populated successfully.")
