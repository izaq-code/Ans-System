import subprocess
from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Conexão com o banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "ans_db"
}

def conectar_db():
    try:
        conexao = mysql.connector.connect(**db_config)
        return conexao
    except mysql.connector.Error as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
        return None


@app.route('/buscar_operadora', methods=['GET'])
def buscar_operadora():
    termo = request.args.get('termo', '')
    conexao = conectar_db()
    
    if not conexao:
        return jsonify({"erro": "Erro ao conectar ao banco de dados"}), 500
    
    cursor = conexao.cursor()
    
    query = "SELECT * FROM operadoras WHERE registro_ans LIKE %s"
    cursor.execute(query, ('%' + termo + '%',))
    resultado = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return jsonify(resultado)

@app.route('/maiores_despesas_trimestre', methods=['GET'])
def maiores_despesas_trimestre():
    conexao = conectar_db()
    if not conexao:
        return jsonify({"erro": "Erro ao conectar ao banco de dados"}), 500
    
    cursor = conexao.cursor()

    query = """
SELECT 
    reg_ans, 
    SUM(vl_saldo_final) AS total_despesa
FROM 
    demonstracoes_contabeis
WHERE 
    descricao = 'EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA À SAÚDE'
    AND data BETWEEN 
        -- Data do início do último trimestre
        CASE
            WHEN MONTH(CURDATE()) IN (1, 2, 3) THEN DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 YEAR), '%Y-10-01') -- Outubro a Dezembro do ano anterior
            WHEN MONTH(CURDATE()) IN (4, 5, 6) THEN DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 QUARTER), '%Y-01-01') -- Janeiro a Março
            WHEN MONTH(CURDATE()) IN (7, 8, 9) THEN DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 QUARTER), '%Y-04-01') -- Abril a Junho
            WHEN MONTH(CURDATE()) IN (10, 11, 12) THEN DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 QUARTER), '%Y-07-01') -- Julho a Setembro
        END 
    AND CURDATE()
GROUP BY 
    reg_ans
ORDER BY 
    total_despesa DESC
LIMIT 10;

    """
    
    cursor.execute(query)
    resultado = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return jsonify(resultado)


@app.route('/maiores_despesas_ano', methods=['GET'])
def maiores_despesas_ano():
    conexao = conectar_db()
    if not conexao:
        return jsonify({"erro": "Erro ao conectar ao banco de dados"}), 500
    
    cursor = conexao.cursor()

    query = """
    SELECT 
        reg_ans, 
        SUM(vl_saldo_final) AS total_despesa
    FROM 
        demonstracoes_contabeis
    WHERE 
        descricao = 'EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA À SAÚDE'
        AND data BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE()
    GROUP BY 
        reg_ans
    ORDER BY 
        total_despesa DESC
    LIMIT 10;
    """
    
    cursor.execute(query)
    resultado = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
