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

SELECT reg_ans, SUM(vl_saldo_final) AS total_despesa
FROM demonstracoes_contabeis
WHERE descricao = 'EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA À SAÚDE'
AND data BETWEEN 
CASE
  WHEN MONTH(CURDATE()) IN (1, 2, 3) THEN DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 YEAR), '%Y-10-01') -- Outubro a Dezembro do ano anterior
  WHEN MONTH(CURDATE()) IN (4, 5, 6) THEN DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 QUARTER), '%Y-01-01') -- Janeiro a Março
  WHEN MONTH(CURDATE()) IN (7, 8, 9) THEN DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 QUARTER), '%Y-04-01') -- Abril a Junho
  WHEN MONTH(CURDATE()) IN (10, 11, 12) THEN DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 QUARTER), '%Y-07-01') -- Julho a Setembro
END AND CURDATE()
GROUP BY reg_ans
ORDER BY total_despesa DESC
LIMIT 10;

