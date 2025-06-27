import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGODB_URI")

client = MongoClient(uri, server_api=ServerApi('1'))
db = client['education']

#Define JSON Schema for the "aluno" collection
aluno_json_schema = {
                "$jsonSchema" : {
                    "bsonType" : "object",
                    "properties" : {
                    "nascimento" : {
                        "bsonType" : "date"
                    },
                    "situacao" : {
                        "bsonType" : "array",
                        "items" : {
                        "bsonType" : "object",
                        "properties" : {
                            "cdMateria" : {
                            "bsonType" : "long"
                            },
                            "dataColeta" : {
                            "bsonType" : "date"
                            },
                            "dataInicio" : {
                            "bsonType" : "date"
                            },
                            "descSituacao" : {
                            "bsonType" : "string"
                            },
                            "dataFinal" : {
                            "bsonType" : "date"
                            }
                        }
                        }
                    },
                    "racaCor" : {
                        "bsonType" : "string"
                    },
                    "paisNasc" : {
                        "bsonType" : "string"
                    },
                    "_id" : {
                        "bsonType" : "objectId"
                    },
                    "cadastro" : {
                        "bsonType" : "long"
                    },
                    "sexo" : {
                        "bsonType" : "string"
                    },
                    "turma" : {
                        "bsonType" : "object",
                        "properties" : {
                        "nomeEsc" : {
                            "bsonType" : "string"
                        },
                        "nomeTurma" : {
                            "bsonType" : "string"
                        }
                        }
                    },
                    "nee" : {
                        "bsonType" : "string"
                    }
                    },
                    "title" : "aluno"
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
        "bsonType" : "string"
      },
      "nomeDistrito" : {
        "bsonType" : "string"
      },
      "dre" : {
        "bsonType" : "string"
      },
      "ambientes" : {
        "bsonType" : "array",
        "items" : {
          "bsonType" : "object",
          "properties" : {
            "codAmb" : {
              "bsonType" : "long"
            },
            "capacidade" : {
              "bsonType" : "string"
            },
            "descAmb" : {
              "bsonType" : "string"
            },
            "metragem" : {
              "bsonType" : "string"
            }
          }
        }
      },
      "nomeEsc" : {
        "bsonType" : "string"
      },
      "_id" : {
        "bsonType" : "objectId"
      },
      "tipoEsc" : {
        "bsonType" : "string"
      },
      "parceria" : {
        "bsonType" : "object",
        "properties" : {
          "protocolo" : {
            "bsonType" : "string"
          },
          "oscCnpj" : {
            "bsonType" : "string"
          },
          "valorMensal" : {
            "bsonType" : "double"
          },
          "valorMensalIptu" : {
            "bsonType" : "double"
          },
          "verbaLocacao" : {
            "bsonType" : "double"
          },
          "dataTermino" : {
            "bsonType" : "date"
          },
          "dataInicio" : {
            "bsonType" : "date"
          }
        }
      },
      "codInep" : {
        "bsonType" : "long"
      },
      "subpref" : {
        "bsonType" : "string"
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
      "parcerias" : {
        "bsonType" : "array",
        "items" : {
          "bsonType" : "object",
          "properties" : {
            "protocolo" : {
              "bsonType" : "string"
            },
            "valorMensal" : {
              "bsonType" : "double"
            },
            "valorMensalIptu" : {
              "bsonType" : "double"
            },
            "verbaLocacao" : {
              "bsonType" : "double"
            },
            "dataTermino" : {
              "bsonType" : "date"
            },
            "dataInicio" : {
              "bsonType" : "date"
            },
            "escolas" : {
              "bsonType" : "array",
              "items" : {
                "bsonType" : "object",
                "properties" : {
                  "nomeDistrito" : {
                    "bsonType" : "string"
                  },
                  "nomeEsc" : {
                    "bsonType" : "string"
                  },
                  "codInep" : {
                    "bsonType" : "long"
                  }
                }
              }
            }
          }
        }
      },
      "nome" : {
        "bsonType" : "string"
      },
      "_id" : {
        "bsonType" : "objectId"
      },
      "cnpj" : {
        "bsonType" : "string"
      }
    },
    "title" : "osc"
  }
}

if 'osc' in db.list_collection_names():
    db.osc.drop()

# Create the collection with schema validation
db.create_collection('osc', validator=osc_json_schema)

#Define JSON Schema for the "turma" collection
turma_json_schema = {
  "$jsonSchema" : {
    "bsonType" : "object",
    "properties" : {
      "etapaEnsino" : {
        "bsonType" : "string"
      },
      "vagas" : {
        "bsonType" : "int"
      },
      "serie" : {
        "bsonType" : "object",
        "properties" : {
          "descricaoSerie" : {
            "bsonType" : "string"
          },
          "codSerie" : {
            "bsonType" : "long"
          },
          "modalidade" : {
            "bsonType" : "string"
          }
        }
      },
      "tipoTurma" : {
        "bsonType" : "string"
      },
      "nomeEsc" : {
        "bsonType" : "string"
      },
      "_id" : {
        "bsonType" : "objectId"
      },
      "turno" : {
        "bsonType" : "object",
        "properties" : {
          "descricaoTurno" : {
            "bsonType" : "string"
          },
          "codTurno" : {
            "bsonType" : "long"
          }
        }
      },
      "matriculados" : {
        "bsonType" : "int"
      },
      "cicloEnsino" : {
        "bsonType" : "string"
      },
      "nomeTurma" : {
        "bsonType" : "string"
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
