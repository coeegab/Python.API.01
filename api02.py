# Importa a biblioteca 'json'.
import json

items = [{
    "id": 1,
    "name": "Bagulho",
    "description": "Apenas um bagulho",
    "location": "Em uma caixa"
}, {
    "id": 2,
    "name": "Tranqueira",
    "description": "Apenas uma tranqueira qualquer",
    "location": "Em um gaveteiro"
}, {
    "id": 3,
    "name": "Bagulete",
    "description": "Um bagulete qualquer",
    "location": "Na esquina"
}]


# Função que lê e lista todos os itens da coleção.
def get_all():
    # Converte a lusta 'items' para json e armazena em 'var_json'
    return json.dumps(items, indent=2)


# Função que lê um item específico, identificado pelo índice.
def get_one(id):

    # Converte o dicionario 'items[id]' para json e armazena em 'var_json'
    var_json = json.dumps(items[id], indent=2)

    # Imprime o json.
    return(var_json)


print(get_all())

print(get_one(1))
