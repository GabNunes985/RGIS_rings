


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


cursor.execute("SELECT nome,senha,badge,id FROM users")
        
users = cursor.fetchall()


print(users)