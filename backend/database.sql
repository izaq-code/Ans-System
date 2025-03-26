CREATE DATABASE ans_db;
USE ans_db;

CREATE TABLE operadoras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cnpj VARCHAR(20) NOT NULL,
    registro_ans VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ano INT NOT NULL,
    trimestre INT NOT NULL,
    data DATE,
    reg_ans VARCHAR(20),
    cd_conta_contabil VARCHAR(50),
    descricao VARCHAR(255),
    vl_saldo_inicial DECIMAL(15,2),
    vl_saldo_final DECIMAL(15,2)
);

SELECT reg_ans, SUM(vl_saldo_final) AS total_despesas
FROM demonstracoes_contabeis
WHERE descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE'
  AND data BETWEEN DATE_SUB(CURDATE(), INTERVAL 3 MONTH) AND CURDATE()
GROUP BY reg_ans
ORDER BY total_despesas DESC
LIMIT 10;

SELECT reg_ans, SUM(vl_saldo_final) AS total_despesas
FROM demonstracoes_contabeis
WHERE descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE'
  AND YEAR(data) = YEAR(CURDATE()) - 1
GROUP BY reg_ans
ORDER BY total_despesas DESC
LIMIT 10;

