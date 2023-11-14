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



def get_all():# Função que lê e lista todos os itens da coleção.
    
    # Converte a lusta 'items' para json e armazena em 'var_json'
    return json.dumps(items, indent=2)



def get_one(id):# Função que lê um item específico, identificado pelo índice.

    for item in items: 
        if item.get("id") == id:
            return json.dumps(item, indent=2)



print(get_all())

print(get_one(1))
