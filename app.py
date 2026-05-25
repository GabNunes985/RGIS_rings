


from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import os
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)



cnx = mysql.connector.connect(
    user= "root",
    password= "gYAhvOFskdkEVGSgnjteTCFtBcRVTnkI",
    host= "kodama.proxy.rlwy.net",
    port= 50348,
    database= "railway",
    
)

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
    

app.secret_key = 'uma_chave_secreta_e_muito_segura_aqui'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificamos se o 'usuario_id' (ou qualquer outra chave) existe na sessão
        if 'usuario' not in session:
            # Se não estiver logado, redireciona para a rota da função 'login'
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    cursor.execute("SELECT nome, senha, badge ,id FROM users")
        
    users = cursor.fetchall()
    
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        
        # Sua lógica de validação (exemplo simples)
        for i in users:
            user =  i[0]
            cpf = i[1]
            badge = i[2]
            id = i[3]
            print(i)
    
            if usuario == badge and senha == cpf:
                # Salva o usuário na sessão (agora ele está "logado")
                session['usuario'] = user
                session['user_id'] = id
                print(id)
                return redirect(url_for('home'))
        else:
                # Se errar, você pode passar uma mensagem de erro para o HTML
                return render_template('login.html', erro="Usuário ou senha incorretos")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Remove o usuário da sessão, efetivamente deslogando-o
    session.pop('usuario', None) 
    
    # Redireciona imediatamente para a tela de login
    return redirect(url_for('login'))


@app.route('/home',methods=['GET'])  
@login_required
def home():

    return render_template('index.html',resultado = '')



@app.route('/home1',methods=['POST'])
@login_required
def data_receiver():
    if request.method == 'POST':
        palavra = 'kapa close'
        texto = request.form.get('texto')
        resultado_final = palavra+texto
    return render_template('index.html',resultado=resultado_final)


@app.route('/rings')
@login_required # Lembra de proteger a rota
def rings():
    # Exemplo usando mysql.connector:
    # conn = obter_conexao()
    # cursor = conn.cursor(dictionary=True)
    
    # IMPORTANTE: O 'ORDER BY nota_media DESC' traz as maiores notas primeiro!
    
    
    array = [5,1,7,8,9,10,'texto',3.5]
    
    
    
    query = f"SELECT id, numero from rings;"
    cursor.execute(query)
    rings = cursor.fetchall()
    print(rings)
    rings_tratados = []
    for ring in rings:
    
        query = f"SELECT nota FROM avaliacoes WHERE rings_id = {ring[0]};"
        
        cursor.execute(query)
        notas_rings = cursor.fetchall()
        contador = 0
        nota = 0
        for item in notas_rings:
            
            nota += item[0]
            contador+=1
        
        media_nota = nota/contador
        rings_tratados.append({"nome":ring[1],"nota_media":media_nota,"id":ring[0]})

    rings_tratados.sort(key=lambda x: x['nota_media'], reverse=True)
    
    print(rings_tratados)
    return render_template('rings.html', lista_rings=rings_tratados)



@app.route('/rings/avaliar', methods=['GET', 'POST'])
@login_required
def nova_avaliacao():
    if request.method == 'POST':
        cursor = cnx.cursor()

        # Pega os dados do formulário HTML
        ring = request.form.get('ring_n')
        nota = request.form.get('nota')
        comentario = request.form.get('comentario')
        
        # O ID do usuário logado você puxa direto da sessão!
        users_id = session.get('user_id') # ou como você salvou no login
        
        # Chama a função de INSERT enviando as variáveis
        
        print(ring)
        query = """
                SELECT id,numero from rings
                """
                
        cursor.execute(query)
        
        rings = cursor.fetchall()
        
        for item in rings:
            
            if item[1] == ring:
                found = True
                break
            else:
                found = False
        if len (rings) == 0:
            found = False
        
        
        if not found:
            
            query = """
                    INSERT IGNORE INTO rings (numero)
                    VALUES(%s)
                    """
            
            cursor.execute(query,(ring,))
            cnx.commit()
        
        query = """
                SELECT id,numero from rings
                """
                
        cursor.execute(query)
        
        rings = cursor.fetchall()
        for i in rings:
            print(i)
            if i[1] == ring:
                ring = i[0]
                break
        
       
       
       
       
       
       
        
        values = (users_id, ring, nota, comentario)
        print(values)
        
        query = """
                INSERT INTO avaliacoes (users_id,rings_id,nota,comentario)
                VALUES (%s , %s, %s, %s)
                """
        
        cursor.execute(query,values)
        cnx.commit()
        cursor.close()
        
        
        if values:
            return redirect(url_for('rings'))
        else:
            return "Erro ao salvar. Talvez você já tenha avaliado esse Ring."

    return render_template('avaliacao.html')

@app.route('/rings/<int:id_do_ring>')
def detalhes_ring(id_do_ring):
    
    cursor = cnx.cursor()
    
    cursor.execute("SELECT numero FROM rings WHERE id = %s", (id_do_ring,))
    ring_atual = cursor.fetchone()
    
    # Se o ring não existir no banco, volta para a lista
    if not ring_atual:
        cursor.close()
        
        return redirect(url_for('rings'))
    
    
    
    query = f"SELECT users_id,nota,comentario FROM avaliacoes WHERE rings_id = {id_do_ring}"

    cursor.execute(query)
    historico_avaliacoes = cursor.fetchall()
    
    avaliacoes = []
    for item in historico_avaliacoes:
        
        print(item)
        query = f"SELECT nome FROM users WHERE id = {item[0]}"
        cursor.execute(query)
        users = cursor.fetchall()
        
        
        avaliacoes.append({'user':users[0][0],
                           'nota':item[1],
                           'comentario':item[2]       
                           })
    
    
        
    cursor.close()
    
    print(avaliacoes)
    
    ring_atual = ring_atual[0]
    
    # Envia o Ring e a lista de avaliações dele para o HTML
    return render_template('detalhes_ring.html', ring=ring_atual, avaliacoes=avaliacoes)





if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

                                     
    
    


