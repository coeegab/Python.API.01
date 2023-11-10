# Importa a biblioteca 'json'.
import json

items = [
    {
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
},   {
    "id": 4,
    "name": "Beligol",
    "description": "Um monstro",
    "location": "Em madrid"
},
{
    "id": 5,
    "name": "Leticya",
    "description": "Uma princesa",
    "location": "Em cosmos"
}
,
{
    "id": 6,
    "name": "Gab",
    "description": "Um Deus grego",
    "location": "Em casa"
}
]



def get_all():# Função que lê e lista todos os itens da coleção.
    
    # Converte a lusta 'items' para json e armazena em 'var_json'
    return json.dumps(items, indent=2)



def get_one(id):# Função que lê um item específico, identificado pelo índice.
    try:
        id = int(id)
        for item in items: 
            if item.get("id") == id:
                return json.dumps(item, indent=2)
    except:
        return False    




def get_data():

    input_id =input("Digite o ID do item:")
    view = get_one(input_id)
    
    if view:
        print(view)
        
    else:
        print("Algo de errado não deu certo")
# get_all()

# get_data()

def new(json_data):
    # print('new →'json_data)
    
    next_id = max(item["id"] for item in items) + 1
    print('max →', next_id)
    return



my_json = '''
    
     {
    "name": "Gongolo",
    "description": "Um piolho e cobra",
    "location": "No jardin"
}
'''

new(my_json)