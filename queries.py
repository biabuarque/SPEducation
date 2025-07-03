import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGODB_URI")
# Create a new client and connect to the server
client = MongoClient('mongodb://localhost:27017/')
db = client['education']

collection = db['escola']
collection.create_index({ "nomeEsc": 1})
collection.create_index({ "nomeDistrito": 1})

collection = db['aluno']
collection.create_index({ "turma.nomeEsc": 1})
collection.create_index({ "racaCor": 1, "paisNasc": 1})
collection.create_index({ "nee": 1})

collection = db['osc']
collection.create_index({ "escolas.nomeEsc": 1, "escolas.nomeDistrito": 1 })

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
# Define aggregation pipelines
pipelines = [
    # QUERY 1
    [
        {"$lookup": {
            "from": "escola",
            "let": { "escolaNames": {
                "$map": {
                    "input": { "$ifNull": ["$escolas", []] },
                    "as": "esc",
                    "in": "$$esc.nome_esc"
                }}
            },
            "pipeline": [
                {
                    "$match": {
                        "$expr": {"$in": ["$nome_esc", "$$escolaNames"]} 
                    }
                }
            ],
            "as": "escola"
        }},
        { "$unwind": "$escola" },
        { "$match": { "escola.dre": { "$ne": None } } },
        {"$group": {
            "_id": {
                "dre": "$escola.dre",
                "race": "$raca_cor",
                "birth_country": "$pais_nasc"
            },
            "total_students": { "$sum": 1 }
        }},
        { "$sort": { "total_students": -1 } },
        {"$project": {
            "birth_country": "$_id.birth_country",
            "race": "$_id.race",
            "dre": "$_id.dre",
            "total_students": 1,
            "_id": 0
        }}
    ],
    # QUERY 2
    [   {"$lookup": {
            "from": "escola",
            "let": { "escolaNames": {
                "$map": {
                    "input": { "$ifNull": ["$escolas", []] },
                    "as": "esc",
                    "in": "$$esc.nome_esc"
                }}
            },
            "pipeline": [
                {
                    "$match": {
                        "$expr": {"$in": ["$nome_esc", "$$escolaNames"]} 
                    }
                }
            ],
            "as": "escola"}
        },
        {"$unwind": "$escola"},
        {"$match": {"nee": {"$ne": None}}},
        {"$group": {
        "_id": {"dre": "$escola.dre", "nee": "$nee"},
        "total_students": {"$sum": 1}
    }},
        {"$project": {
            "dre": "$_id.dre",
            "nee": "$_id.nee",
            "total_students": 1,
            "_id": 0
        }},
        {"$sort": {"total_students": -1, "dre": 1}}
    ],
    # QUERY 3
    [
        {"$lookup": {
            "from": "escola",
            "localField": "nome_esc",
            "foreignField": "nome_esc",
            "as": "escola"
        }},
        {"$unwind": "$escola"},
        {"$addFields": {
            "open_spaces": {
                "$subtract": [
                    {"$ifNull": ["$vagas", 0]}, 
                    {"$ifNull": ["$matriculados", 0]}  
                ]
            }
        }},
        {"$group": {
            "_id": {"dre": "$escola.dre", "school": "$nome_esc"},
            "open_spaces": {"$first": "$open_spaces"}
        }},
        {"$project": {
            "dre": "$_id.dre",
            "school": "$_id.school",
            "open_spaces": 1,
            "_id": 0
        }},
        {"$sort": {"open_spaces": -1, "dre": 1}}
    ],
    #  QUERY 4
    [   
        {"$lookup": {
            "from": "osc",
            "let": { "cnpjs": {
                "$map": {
                    "input": { "$ifNull": ["$parcerias", []] },
                    "as": "par",
                    "in": "$$par.osc_cnpj"
                }}
            },
            "pipeline": [
                {
                    "$match": {
                        "$expr": {"$in": ["$cnpj", "$$cnpjs"]} 
                    }
                }
            ],
            "as": "osc"}
        },
        {"$unwind": "$osc"},
        {"$unwind": "$ambientes"},
        {"$group": {
            "_id": {"school": "$nome_esc", "ambient": "$ambientes.descAmb", "parceria": "$osc.nome_osc"},
            "total_ambients": {"$sum": 1}
        }},
        {"$project": {
            "school": "$_id.school",
            "parceria": "$_id.parceria",
            "ambient": "$_id.ambient",
            "total_ambients": 1,
            "_id": 0
        }},
        {"$sort": {"total_ambients": 1, "school": 1, "ambient": 1}}
    ],
    #   QUERY 5
     [  {"$lookup": {
            "from": "escola",
            "let": { "escolaNames": {
                "$map": {
                    "input": { "$ifNull": ["$escolas", []] },
                    "as": "esc",
                    "in": "$$esc.nome_esc"
                }}
            },
            "pipeline": [
                {
                    "$match": {
                        "$expr": {"$in": ["$nome_esc", "$$escolaNames"]} 
                    }
                }
            ],
            "as": "escola"}
        },
        {"$unwind": "$escola"},
        {"$match": {"data_nasc": {"$ne": None}}},
        {"$addFields": {
            "current_date": {
                "$dateFromString": {
                    "dateString": "2025-01-01", 
                    "format": "%Y-%m-%d"
                }
            }
        }},
        
        {"$addFields": {
            "age": {
                "$subtract": [
                    {"$year": "$current_date"}, 
                    {"$year": "$data_nasc"}  
                ]
            }
        }},
        {"$group": {
            "dre": {"$first": "$escola.dre"},
            "_id": "$escola.nome_esc",
            "average_age": {"$avg": "$age"}  
        }},
        {"$project": {
            "dre": 1,
            "school": "$_id",
            "average_age": {"$round": ["$average_age", 0]},
            "_id": 0
        }},
        {"$sort": {"average_age": -1}}
    ]
]

already_done = [1, 2, 3, 4]
# Execute each pipeline and export results to CSV
for i, pipeline in enumerate(pipelines, 1):
    if i in already_done:
        print(f"Query {i} already done, skipping...")
        continue
    collection_name = ["aluno", "aluno", "turma", "escola", "aluno"][i-1]
    collection = db[collection_name]
    results = collection.aggregate(pipeline)
    df = pd.DataFrame(list(results))
    df.to_csv(f"query_{i}.csv", index=False)
    print(f"Query {i} results saved to query_{i}.csv")

client.close()
