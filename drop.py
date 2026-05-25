





from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import os
import mysql.connector
from mysql.connector import Error




cnx = mysql.connector.connect(
    user= "root",
    password= "gYAhvOFskdkEVGSgnjteTCFtBcRVTnkI",
    host= "kodama.proxy.rlwy.net",
    port= 50348,
    database= "railway",
    
)

cursor = cnx.cursor()









query = """
DROP table avaliacoes
"""

cursor.execute(query)

query = """
DROP table rings
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
        UNIQUE(users_id, rings_id))
"""

cursor.execute(query)