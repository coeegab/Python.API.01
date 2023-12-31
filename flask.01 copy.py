# -*- coding: utf-8 -*-

# Importa bibliotecas.
from flask import Flask, jsonify, request, abort, make_response, json, Response
import sqlite3

# Cria aplicativo Flask.
app = Flask(__name__)

# Configura o character set das transações HTTP para UTF-8.
json.provider.DefaultJSONProvider.ensure_ascii = False

# Especifica a base de dados SQLite3.
database = "./dbitem.db"


def prefix_remove(prefix, data):

    # Função que remove os prefixos dos nomes dos campos de um 'dict'.
    # Por exemplo, prefix_remove('item_', { 'item_id': 2, 'item_name': 'Coisa', 'item_status': 'on' })
    # retorna { 'id': 2, 'name': 'Coisa', 'status': 'on' }
    # Créditos: Comunidade StackOverflow.

    new_data = {}
    for key, value in data.items():
        if key.startswith(prefix):
            new_key = key[len(prefix):]
            new_data[new_key] = value
        else:
            new_data[key] = value
    return new_data


@app.route("/owners", methods=["GET"])
def get_all_owners():

    # Obtém todos os registros válidos de 'item'.
    # Request method → GET
    # Request endpoint → /owner
    # Response → JSON

    try:

        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)

        # Formata os dados retornados na factory como SQLite.Row.
        conn.row_factory = sqlite3.Row

        # Cria um cursor de dados.
        cursor = conn.cursor()

        # Executa o SQL.
        cursor.execute(
            "SELECT * FROM owner WHERE owner_status != 'off' ORDER BY owner_name COLLATE NOCASE ASC")

        # Retorna todos os resultados da consulta para 'owner_rows'.
        owner_rows = cursor.fetchall()

        # Fecha a conexão com o banco de dados
        conn.close()

        # Cria uma lista para armazenar os registros.
        owners = []

        # Converte cada SQLite.Row em um dicionário e adiciona à lista 'registros'.
        for owner in owner_rows:
            owners.append(dict(owner))

        # Verifica se há registros antes de retornar...
        if owners:

            # Remove prefixos dos campos.
            new_owners = [prefix_remove('owner_', owner) for owner in owners]

            # Se houver registros, retorna tudo.
            return new_owners, 200
        else:
            # Se não houver registros, retorna erro.
            return {"error": "Nenhum item encontrado"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route("/owner/<int:id>", methods=["GET"])
def get_one(id):

    # Obtém um registro único de 'item', identificado pelo 'id'.
    # Request method → GET
    # Request endpoint → /items/<id>
    # Response → JSON

    try:
        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Executa o SQL.
        cursor.execute(
            "SELECT * FROM owner WHERE owner_id = ? AND owner_status = 'on'",
            (id, ))

        # Retorna o resultado da consulta para 'item_row'.
        owner_row = cursor.fetchone()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Se o registro existe...
        if owner_row:

            # Converte SQLite.Row para dicionário e armazena em 'item'.
            owner = dict(owner_row)

            # Remove prefixos dos campos.
            new_owner = prefix_remove('owner_', owner)

            # Retorna item.
            return new_owner, 200
        else:
            # Se não encontrar o registro, retorna erro.
            return {"error": "Item não encontrado"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route('/owner', methods=["POST"])
def create():

    # Cadastra um novo registro em 'item'.
    # Request method → POST
    # Request endpoint → /items
    # Request body → JSON (raw) → { String:name, String:description, String:location, int:owner }
    # Response → JSON → { "success": "Registro criado com sucesso", "id": id do novo registro }}

    try:
        # Recebe dados do body da requisição na forma de 'dict'.
        new_owner = request.get_json()

        # Conecta ao banco de dados.
        # Observe que 'row_factory' é desnecessário porque não receberemos dados do banco de dados.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Query que insere um novo registro na tabela 'item'.
        sql = "INSERT INTO owner (owner_name, owner_email, owner_password, owner_birth) VALUES (?, ?, ?, ?)"

        # Dados a serem inseridos, obtidos do request.
        sql_data = (new_owner['name'], new_owner['email'],
                    new_owner['password'], new_owner['birth'])

        # Executa a query, fazendo as devidas substituições dos curingas (?) pelos dados (sql_data).
        cursor.execute(sql, sql_data)

        # Obter o ID da última inserção
        inserted_id = int(cursor.lastrowid)

        # Salvar as alterações no banco de dados.
        conn.commit()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Retorna com mensagem de sucesso e status HTTP "201 Created".
        return {
            "success": "Registro criado com sucesso",
            "id": inserted_id
        }, 201

    except json.JSONDecodeError as e:  # Erro ao obter dados do JSON.
        return {"error": f"Erro ao decodificar JSON: {str(e)}"}, 500

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route("/owner/<int:id>", methods=["DELETE"])
def delete(id):

    # Marca, como apagado, um registro único de 'item', identificado pelo 'id'.
    # Request method → DELETE
    # Request endpoint → /items/<id>
    # Response → JSON → { "success": "Registro apagado com sucesso", "id": id do registro }

    try:

        # Conecta ao banco de dados.
        # Observe que 'row_factory' é desnecessário porque não receberemos dados do banco de dados.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Query que pesquisa a existência do registro.
        sql = "SELECT owner_id FROM owner WHERE owner_id = ? AND owner_status != 'off'"

        # Executa a query.
        cursor.execute(sql, (id, ))

        # Retorna o resultado da consulta para 'item_row'.
        owner_row = cursor.fetchone()

        # Se o registro exite e está ativo...
        if owner_row:

            # Query para atualizar o item no banco de dados.
            sql = "UPDATE owner SET owner_status = 'off' WHERE owner_id = ?"

            # Executa a query.
            cursor.execute(sql, (id, ))

            # Salvar no banco de dados.
            conn.commit()

            # Fecha o banco de dados.
            conn.close()

            # Retorna com mensagem de sucesso e status HTTP "200 Ok".
            return {"success": "Registro apagado com sucesso", "id": id}, 200

        # Se o registro não existe, não pode ser apagado.
        else:

            # Fecha o banco de dados.
            conn.close()

            # Retorna mensagem de erro 404.
            return {"error": "Item não existe"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route("/owner/<int:id>", methods=["PUT", "PATCH"])
def edit(id):

    # Edita um registro em 'item', identificado pelo 'id'.
    # Request method → PUT ou PATCH
    # Request endpoint → /items/<id>
    # Request body → JSON (raw) → { String:name, String:description, String:location, int:owner }
    #       OBS: usando "PATCH", não é necessário enviar todos os campos, apenas os que serão alterados.
    # Response → JSON → { "success": "Registro atualizado com sucesso", "id": id do registro }

    try:

        # Recebe os dados do corpo da requisição.
        owner_json = request.get_json()

        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Loop para atualizar os campos específicos do registro na tabela 'item'.
        # Observe que o prefixo 'item_' é adicionado ao(s) nome(s) do(s) campo(s).
        set_clause = ', '.join(
            [f"owner_{key} = ?" for key in owner_json.keys()])

        # Monta SQL com base nos campos a serem atualizados.
        sql = f"UPDATE owner SET {set_clause} WHERE owner_id = ? AND owner_status = 'on'"
        cursor.execute(sql, (*owner_json.values(), id))

        # Commit para salvar as alterações.
        conn.commit()

        # Fechar a conexão com o banco de dados.
        conn.close()

        # Confirma a atualização.
        return {"success": "Registro atualizado com sucesso", "id": id}, 201

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500
    
@app.route("/owner/<int:id>/items", methods=["GET"])
def get_items_by_owner(id):

    # Obtém todos os itens cadastrados para um proprietário específico.
    # Request method → GET
    # Request endpoint → /owners/<id>/items
    # Response → JSON

    try:
        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Executa o SQL para obter os itens do proprietário específico.
        cursor.execute(
            "SELECT * FROM item WHERE item_owner = ? AND item_status != 'off'",
            (id,))

        # Retorna todos os resultados da consulta para 'item_rows'.
        item_rows = cursor.fetchall()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Se houver itens, converte cada SQLite.Row em um dicionário.
        if item_rows:
            items = [dict(item) for item in item_rows]

            # Remove prefixos dos campos.
            new_items = [prefix_remove('item_', item) for item in items]

            # Retorna a lista de itens do proprietário.
            return new_items, 200
        else:
            # Se não houver itens, retorna uma mensagem de erro.
            return {"error": "Nenhum item encontrado para o proprietário"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500
    
@app.route("/owners/<int:id>/items", methods=["GET"])
def get_items_with_owners(id):
    try:
        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Executa a consulta SQL com INNER JOIN.
        cursor.execute('''
            SELECT *
            FROM item
            INNER JOIN owner ON item_owner = owner_id WHERE item_status !='off' and item_id = ?
        ''', (id,))

        # Obtém todos os resultados da consulta.
        results = cursor.fetchone()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Retorna os resultados.
        return dict(results)

    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {str(e)}")

    #return {"olá": "mundo"}


# Roda aplicativo Flask.
if __name__ == "__main__":
    app.run(debug=True)
