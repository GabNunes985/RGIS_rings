


from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import os
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def cnn():

    cnx = mysql.connector.connect(
        user= "root",
        password= "gYAhvOFskdkEVGSgnjteTCFtBcRVTnkI",
        host= "kodama.proxy.rlwy.net",
        port= 50348,
        database= "railway",
        
    )
    return cnx
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
    if 'usuario' in session:
            # Se não estiver logado, redireciona para a rota da função 'login'
            return redirect(url_for('home'))
    cnx = cnn()
    cursor = cnx.cursor()


    cursor.execute("SELECT nome,senha,badge,id FROM users")
            
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
                cnx.close()
                cursor.close()
                
                return redirect(url_for('home'))
        
        cnx.close()
        cursor.close()
        # Se errar, você pode passar uma mensagem de erro para o HTML
        return render_template('login.html', erro="Usuário ou senha incorretos")
        
    return render_template('login.html')







@app.route('/')
@login_required
def index():
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    # Remove o usuário da sessão, efetivamente deslogando-o
    session.pop('usuario', None) 
    
    # Redireciona imediatamente para a tela de login
    return redirect(url_for('login'))


@app.route('/home',methods=['GET'])  
@login_required
def home():

    return render_template('index.html',resultado = '',pagina_atual='home')



@app.route('/home1',methods=['POST'])
@login_required
def data_receiver():
    if request.method == 'POST':
        palavra = 'kapa close'
        texto = request.form.get('texto')
        resultado_final = palavra+texto
    return render_template('index.html',resultado=resultado_final)


@app.route('/rings')
@login_required 
def rings():
    
    cnx = cnn()
    cursor = cnx.cursor()
    
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

        if contador == 0:
         media_nota = 0
        else:
         media_nota = nota/contador
        
        rings_tratados.append({"nome":ring[1],"nota_media":media_nota,"id":ring[0]})

    rings_tratados.sort(key=lambda x: x['nota_media'], reverse=True)
    
    print(rings_tratados)
    cnx.close()
    cursor.close()
    
    return render_template('rings.html', lista_rings=rings_tratados)



@app.route('/rings/avaliar', methods=['GET', 'POST'])
@login_required
def nova_avaliacao():
    if request.method == 'POST':
        
        cnx = cnn()
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
        
        try:
            
            cursor.execute(query,values)
            cnx.commit()
            
        except:
            cnx.close()
            cursor.close()
            return '''
                <script>
                    alert("Você já avaliou esse ring!!");
                    window.location.href = document.referrer; // Faz o navegador voltar para a página de onde o usuário veio
                </script>
                '''
        
        if values:
            cnx.close()
            cursor.close()
            return redirect(url_for('rings'))
        else:
            cnx.close()
            cursor.close()
            return "Erro ao salvar. Talvez você já tenha avaliado esse Ring."
    
    return render_template('avaliacao.html')

@app.route('/rings/<int:id_do_ring>')
def detalhes_ring(id_do_ring):
    
    cnx = cnn()
    
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
    cnx.close()
    cursor.close()
    # Envia o Ring e a lista de avaliações dele para o HTML
    return render_template('detalhes_ring.html', ring=ring_atual, avaliacoes=avaliacoes)


# -------------------------------------------------------------
# ROTA 1: EXIBIR O HISTÓRICO DO USUÁRIO LOGADO
# -------------------------------------------------------------
@app.route('/meu-historico')
@login_required
def meu_historico():
    users_id = session.get('user_id') # Pega o ID de quem está logado
    
    conn = cnn()
    cursor = conn.cursor(dictionary=True)
    
    # Busca apenas as avaliações do usuário logado fazendo JOIN com rings para saber o número do equipamento
    query = """
        SELECT 
            avaliacoes.id,
            avaliacoes.nota,
            avaliacoes.comentario,
            DATE_FORMAT(avaliacoes.data_avaliacao, '%d/%m/%Y') as data_formatada,
            rings.numero AS numero_ring
        FROM avaliacoes
        INNER JOIN rings ON avaliacoes.rings_id = rings.id
        WHERE avaliacoes.users_id = %s
        ORDER BY avaliacoes.data_avaliacao DESC
    """
    cursor.execute(query, (users_id,))
    minhas_avaliacoes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('meu_historico.html', avaliacoes=minhas_avaliacoes,pagina_atual='historico')


# -------------------------------------------------------------
# ROTA 2: DELETAR UMA AVALIAÇÃO
# -------------------------------------------------------------
@app.route('/avaliacao/deletar/<int:id_avaliacao>')
@login_required
def deletar_avaliacao(id_avaliacao):
    users_id = session.get('user_id')
    
    conn = cnn()
    cursor = conn.cursor()
    
    # O 'AND users_id = %s' garante que o usuário só consiga deletar as avaliações DELE MESMO
    query = "DELETE FROM avaliacoes WHERE id = %s AND users_id = %s"
    cursor.execute(query, (id_avaliacao, users_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('meu_historico'))


# -------------------------------------------------------------
# ROTA 3: EDITAR UMA AVALIAÇÃO (GET para abrir a tela, POST para salvar)
# -------------------------------------------------------------
@app.route('/avaliacao/editar/<int:id_avaliacao>', methods=['GET', 'POST'])
def editar_avaliacao(id_avaliacao):
    users_id = session.get('user_id')
    
    conn = cnn()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        # Recebe os dados atualizados do formulário
        nova_nota = request.form.get('nota')
        novo_comentario = request.form.get('comentario')
        
        query_update = """
            UPDATE avaliacoes 
            SET nota = %s, comentario = %s 
            WHERE id = %s AND users_id = %s
        """
        cursor.execute(query_update, (nova_nota, novo_comentario, id_avaliacao, users_id))
        conn.commit()
        
        cursor.close()
        conn.close()
        return redirect(url_for('meu_historico'))
        
    # Se for GET, busca os dados atuais da avaliação para preencher a tela de edição
    query_busca = """
        SELECT avaliacoes.*, rings.numero AS numero_ring 
        FROM avaliacoes 
        INNER JOIN rings ON avaliacoes.rings_id = rings.id
        WHERE avaliacoes.id = %s AND avaliacoes.users_id = %s
    """
    cursor.execute(query_busca, (id_avaliacao, users_id))
    avaliacao_atual = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    # Aqui você pode reaproveitar a sua estrutura de formulário (add_avaliacao) adaptando os campos!
    return render_template('edit_avaliacao.html', avaliacao=avaliacao_atual)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

                                     
    
    