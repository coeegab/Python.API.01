import json
import sqlite3
import os


def get_one_owner(id):
    database = './dbitem.db'


    # Incializa o banco de dados.
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query de consulta.
    sql = "SELECT * FROM owner WHERE owner_status != 'off' AND owner_id = ?"

    # Executa o código passando o valor do ID.
    cursor.execute(sql, (id,))

    # Retorna o resultado da busca para 'data'.
    data = cursor.fetchone()

    # Fecha a conexão com o banco de dados.
    conn.close()

    if data:  # Se o registro existir...

        # Retorna o registro em um 'dict'.
        return dict(data)

    else:  # Se o registro não chegou...

        # Retorna erro.
        return {"error": "Registro não encontrado."}


# Limpa o console.
os.system('cls')

# Exemplo para obter todos os 'item' válidos.
# print(  # Exibe no console.
#     json.dumps(  # No formato JSON.
#         get_all_items(),  # Os items obtidos desta função.
#         ensure_ascii=False,  # Usando a tabela UTF-8 (acentuação).
#         indent=2  # Formatando o JSON.
#     )
# )

# Exemplo para obter um 'item' pelo ID.
print(
    json.dumps(
        get_one_owner(7),
        ensure_ascii=False,
        indent=2
    )
)
