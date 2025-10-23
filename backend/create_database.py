import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    try:
        # Conectar ao PostgreSQL (banco padrão)
        conn = psycopg2.connect(
            host="localhost",
            user="postgres", 
            password="postgres",
            port="5432"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar se o banco já existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='cardio_ml_db'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute("CREATE DATABASE cardio_ml_db")
            print("[OK] Banco de dados 'cardio_ml_db' criado com sucesso!")
        else:
            print("[INFO] Banco de dados 'cardio_ml_db' ja existe.")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"[ERRO] Erro ao criar banco: {e}")
        print("Certifique-se de que o PostgreSQL está rodando e as credenciais estão corretas.")

if __name__ == "__main__":
    create_database()