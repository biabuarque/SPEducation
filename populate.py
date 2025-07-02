import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import json

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['education']  # Replace 'your_database' with your database name

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

# Function to process a json file and insert data into MongoDB
def populate_collection(json_path, collection, schema_mapping):

    # Read the json file where each line is a JSON object
    schema_mapping = schema_mapping['$jsonSchema']['properties']
    with open(json_path, 'r') as file:
        counter = 0
        line_count = sum(1 for _ in open(json_path, 'r'))  # Count the number of lines in the file

        for line in file:
            print(f"Processing line {counter + 1} of {line_count} in {json_path}... {counter/line_count * 100:.2f}% complete", end='\r')
            counter += 1
            data = json.loads(line)

            # Process each field according to the schema mapping
            for field, properties in schema_mapping.items():
                if field in data:
                    types_now = properties.get('bsonType')
                    # Convert date strings to datetime objects
                    if ('date' in types_now) and isinstance(data[field], str):
                        data[field] = process_date(data[field])
                    
                    # Convert numeric fields to appropriate types
                    if ("int" in (types_now) or "long" in types_now) and isinstance(data[field], str):
                        try:
                            data[field] = int(data[field])
                        except ValueError:
                            data[field] = None
                        
                    if "array" in types_now and isinstance(data[field], list):
                        # Process each item in the array if it is an object
                        for item in data[field]:
                            if isinstance(item, dict):
                                for sub_field, sub_properties in properties.get('items', {}).get('properties', {}).items():
                                    if sub_field in item:
                                        sub_types_now = sub_properties.get('bsonType')
                                        # Convert date strings to datetime objects
                                        if ('date' in sub_types_now) and isinstance(item[sub_field], str):
                                            item[sub_field] = process_date(item[sub_field])
                                        
                                        # Convert numeric fields to appropriate types
                                        if ("int" in (sub_types_now) or "long" in sub_types_now) and isinstance(item[sub_field], str):
                                            try:
                                                item[sub_field] = int(item[sub_field])
                                            except ValueError:
                                                item[sub_field] = None
            
            # Insert the processed data into the collection
            collection.insert_one(data)


# Define schema mappings for each collection
aluno_schema = json.load(open("schemas/Aluno_MongoDBSchema.json"))
escola_schema = json.load(open("schemas/Escola_MongoDBSchema.json"))
osc_schema = json.load(open("schemas/Osc_MongoDBSchema.json"))
turma_schema = json.load(open("schemas/Turma_MongoDBSchema.json"))

# Populate each collection
populate_collection('datasets/alunos.json', aluno_collection, aluno_schema)
populate_collection('datasets/turmas.json', turma_collection, turma_schema)
populate_collection('datasets/osc.json', osc_collection, osc_schema)
populate_collection('datasets/escolas.json', escola_collection, escola_schema)

# Close MongoDB connection
client.close()

print("MongoDB populated successfully.")
