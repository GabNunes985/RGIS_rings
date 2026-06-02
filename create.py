
import mysql.connector
from datetime import datetime

cnx = mysql.connector.connect(
    user="root",
    password="gYAhvOFskdkEVGSgnjteTCFtBcRVTnkI",
    host="kodama.proxy.rlwy.net",
    port=50348,
    database="railway"
)




cnx = cnn()
cursor = cnx.cursor()

query = "SHOW TABLES LIKE 'users'"

cursor.execute(query)

if not cursor.fetchone():
    query = """
    CREATE TABLE users(
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100),
        senha VARCHAR (4),
        badge VARCHAR (8)
    )
    """
    cursor.execute(query)
    query = """
    CREATE TABLE rings(
        id SERIAL PRIMARY KEY,
        numero VARCHAR(3)
    )
    """
    cursor.execute(query)
    query = """
        CREATE TABLE IF NOT EXISTS avaliacoes(
        id SERIAL PRIMARY KEY,
        users_id BIGINT UNSIGNED,
        rings_id BIGINT UNSIGNED,
        nota INT CHECK (nota BETWEEN 1 AND 10),
        comentario TEXT,
        data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        
        FOREIGN KEY (users_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (rings_id) REFERENCES rings(id) ON DELETE CASCADE,
        UNIQUE(users_id, rings_id)
    )
    """
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()
    #INSERT INTO users (nome,senha,badge) 
    #VALUES ('Gab', '0534', '91800354')
    
