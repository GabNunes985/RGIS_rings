import mysql.connector
from datetime import datetime

# ================== CONFIGURAÇÃO ==================
cnx = mysql.connector.connect(
    user="root",
    password="gYAhvOFskdkEVGSgnjteTCFtBcRVTnkI",
    host="kodama.proxy.rlwy.net",
    port=50348,
    database="railway"
)

arquivo = f"backup_mysql_{datetime.now().strftime('%Y%m%d_%H%M')}.sql"
# ================================================

cursor = cnx.cursor()

with open(arquivo, 'w', encoding='utf-8') as f:
    f.write("-- Backup Railway MySQL\n")
    f.write(f"-- Gerado em: {datetime.now()}\n\n")
    
    # Desabilita verificação de foreign keys
    f.write("SET FOREIGN_KEY_CHECKS=0;\n\n")
    
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    
    for table in tables:
        print(f"Fazendo backup da tabela: {table}")
        
        # CREATE TABLE
        cursor.execute(f"SHOW CREATE TABLE `{table}`")
        create_table = cursor.fetchone()[1]
        f.write(f"{create_table};\n\n")
        
        # INSERTS
        cursor.execute(f"SELECT * FROM `{table}`")
        rows = cursor.fetchall()
        
        if rows:
            columns = [desc[0] for desc in cursor.description]
            f.write(f"INSERT INTO `{table}` ({', '.join(f'`{col}`' for col in columns)}) VALUES\n")
            
            values_list = []
            for row in rows:
                values = []
                for value in row:
                    if value is None:
                        values.append("NULL")
                    elif isinstance(value, (int, float)):
                        values.append(str(value))
                    else:
                        values.append(f"'{str(value).replace('\'', '\'\'')}'")
                values_list.append("(" + ", ".join(values) + ")")
            
            f.write(",\n".join(values_list) + ";\n\n")
    
    f.write("SET FOREIGN_KEY_CHECKS=1;\n")

cursor.close()
cnx.close()
print(f"✅ Backup concluído! Arquivo salvo: {arquivo}")