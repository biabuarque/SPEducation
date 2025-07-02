import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGODB_URI")

client = MongoClient("mongodb://localhost:27017/")
db = client['education']

aluno_json_schema = {
                "$jsonSchema": {
                  "bsonType": "object",
                  "title": "aluno",
                  "required": ["id_aluno", "cadastro"],
                  "properties": {
                    "id_aluno": {
                      "bsonType": ["objectId", "int"]
                    },
                    "cadastro": {
                      "bsonType": ["long", "int"]
                    },
                    "data_nasc": {
                      "bsonType": ["date", "string", "null"]
                    },
                    "raca_cor": {
                      "bsonType": ["string", "null"]
                    },
                    "pais_nasc": {
                      "bsonType": ["string", "null"]
                    },
                    "sexo": {
                      "bsonType":["string", "null"]
                    },
                    "nee": {
                      "bsonType": ["string", "null"]
                    },
                    "turmas": {
                      "bsonType": ["array", "null"],
                      "items": {
                        "bsonType": "object",
                        "required": ["cd_mat", "data_sit", "situacao_mat", "id_turma"],
                        "properties": {
                          "cd_mat": {
                            "bsonType": ["long", "int"]
                          },
                          "data_sit": {
                            "bsonType": ["date", "string", "null"]
                          },
                          "situacao_mat": {
                            "bsonType":  ["string", "null"]
                          },
                          "id_turma": {
                            "bsonType": ["long", "int"]
                          }
                        }
                      }
                    },
                    "escola": {
                      "bsonType": ["array", "null"],
                      "items": {
                        "bsonType": "object",
                        "properties": {
                          "nome_escola": {
                            "bsonType": ["string", "null"]
                          }
                        }
                      }
                    }
                  }
                }
    }

if 'aluno' in db.list_collection_names():
    db.aluno.drop()

# Create the collection with schema validation
db.create_collection('aluno', validator=aluno_json_schema)

#Define JSON Schema for the "escola" collection
escola_json_schema = {
  "$jsonSchema" : {
    "bsonType" : "object",
    "properties" : {
      "rede" : {
        "bsonType" : ["string", "null"]
      },
      "nome_distrito" : {
        "bsonType" : ["string", "null"]
      },
      "dre" : {
        "bsonType" : ["string", "null"]
      },
      "ambientes" : {
        "bsonType" : ["array", "null"],
        "items" : {
          "bsonType" : "object",
          "properties" : {
            "codAmbiente" : {
              "bsonType" : ["long", "int", "null"]
            },
            "capacidade" : {
              "bsonType" : ["string", "null"]
            },
            "descAmb" : {
              "bsonType" : ["string", "null"]
            },
            "metragem" : {
              "bsonType" : ["string", "null"]
            }
          }
        }
      },
      "nome_esc" : {
        "bsonType" : ["string", "null"]
      },
      "tipo_esc" : {
        "bsonType" : ["string", "null"]
      },
      "parcerias" : {
        "bsonType" : ["array", "null"],
        "items" : {
          "bsonType" : "object",
          "properties" : {
            "protocolo" : {
              "bsonType" : ["string", "null"]
            },
            "osc_cnpj" : {
              "bsonType" : ["string", "null"]
            },
            "valor_mensal" : {
              "bsonType" : ["double", "int", "null"]
            },
            "valor_mensal_iptu" : {
              "bsonType" : ["double", "int", "null"]
            },
            "verba_locação" : {
              "bsonType" : ["double", "int", "null"]
            },
            "data_termino" : {
              "bsonType" : ["date", "string", "null"]
            },
            "data_inicio" : {
              "bsonType" : ["date", "string", "null"]
            }
          }
        }
      },
      "cod_inep" : {
        "bsonType" : ["long", "int", "null"]
      },
      "subpref" : {
        "bsonType" : ["string", "null"]
      }
    },
    "title" : "escola"
  }
}

if 'escola' in db.list_collection_names():
    db.escola.drop()

# Create the collection with schema validation
db.create_collection('escola', validator=escola_json_schema)

#Define JSON Schema for the "osc" collection
osc_json_schema = {
  "$jsonSchema" : {
    "bsonType" : "object",
    "properties" : {
      "nome_osc" : {
        "bsonType" : ["string", "null"]
      },
      "cnpj" : {
        "bsonType" : ["string", "null"]
      },
      "protocolo" : {
        "bsonType" : ["string", "null"]
      },
      "valor_mensal" : {
        "bsonType" : ["double", "int", "null"]
      },
      "valor_mensal_iptu" : {
        "bsonType" : ["double", "int", "null"]
      },
      "verba_locacao" : {
        "bsonType" : ["double", "int", "null"]
      },
      "data_inicio" : {
        "bsonType" : ["date", "string", "null"]
      },
      "data_fim" : {
        "bsonType" : ["date", "string", "null"]
      },
      "escolas" : {
        "bsonType" : ["array", "null"],
        "items" : {
          "bsonType" : "object",
          "properties" : {
            "nome_esc" : {
              "bsonType" : ["string", "null"]
            },
            "tipo_esc" : {
              "bsonType" : ["string", "null"]
            },
            "rede" : {
              "bsonType" : ["string", "null"]
            },
            "nome_distrito" : {
              "bsonType" : ["string", "null"]
            },
            "dre" : {
              "bsonType" : ["string", "null"]
            },
            "subpref" : {
              "bsonType" : ["string", "null"]
            }
          }
        }
      }
    },
    "title" : "osc"
  }
}

if 'osc' in db.list_collection_names():
    db.osc.drop()

# Create the collection with schema validation
db.create_collection('osc', validator=osc_json_schema)

turma_json_schema = {
  "$jsonSchema" : {
    "bsonType" : "object",
    "properties" : {
      "id_turma" : {
        "bsonType" : ["long", "int"]
      },
      "nome_turma" : {
        "bsonType" : ["string", "null"]
      },
      "nome_esc" : {
        "bsonType" : ["string", "null"]
      },
      "desc_turno" : {
        "bsonType" : ["string", "null"]
      },
      "desc_serie" : {
        "bsonType" : ["string", "null"]
      },
      "cod_turno" : {
        "bsonType" : ["long", "int", "null"]
      },
      "cod_serie" : {
        "bsonType" : ["long", "int", "null"]
      },
      "matriculados" : {
        "bsonType" : ["int", "null"]
      },
      "vagas" : {
        "bsonType" : ["int", "null"]
      },
      "ano_letivo" : {
        "bsonType" : ["int", "null"]
      },
      "tipo_turma" : {
        "bsonType" : ["string", "null"]
      },
      "etapa_ensino" : {
        "bsonType" : ["string", "null"]
      },
      "ciclo_ensino" : {
        "bsonType" : ["string", "null"]
      },
      "alunos" : {
        "bsonType" : ["array", "null"],
        "items" : {
          "bsonType" : "object",
          "properties" : {
            "id_aluno" : {
              "bsonType" : ["long", "int"]
            },
            "cd_mat" : {
              "bsonType" : ["long", "int"]
            },
            "data_sit" : {
              "bsonType" : ["date", "string", "null"]
            },
            "situacao_mat" : {
              "bsonType" : ["string", "null"]
            }
          }
        }
      }
    },
    "title" : "turma"
  }
}

if 'turma' in db.list_collection_names():
    db.turma.drop()

# Create the collection with schema validation
db.create_collection('turma', validator=turma_json_schema)

client.close()

print("MongoDB database setup with schema validation is complete!")
