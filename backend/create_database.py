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
        
        # Criar tabelas de usuários
        create_user_tables()
        
    except Exception as e:
        print(f"[ERRO] Erro ao criar banco: {e}")
        print("Certifique-se de que o PostgreSQL está rodando e as credenciais estão corretas.")

def create_user_tables():
    try:
        # Conectar ao banco cardio_ml_db
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="postgres",
            port="5432",
            database="cardio_ml_db"
        )
        cursor = conn.cursor()
        
        # Criar tabela users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                login VARCHAR(50) UNIQUE NOT NULL,
                nome VARCHAR(100) NOT NULL,
                senha_hash VARCHAR(255) NOT NULL,
                token VARCHAR(500),
                token_expires_at TIMESTAMP
            )
        """)
        
        # Criar tabela clinical_cases
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clinical_cases (
                id SERIAL PRIMARY KEY,
                age INTEGER NOT NULL,
                gender INTEGER NOT NULL,
                height INTEGER NOT NULL,
                weight INTEGER NOT NULL,
                ap_hi INTEGER NOT NULL,
                ap_lo INTEGER NOT NULL,
                cholesterol INTEGER NOT NULL,
                gluc INTEGER NOT NULL,
                smoke INTEGER NOT NULL,
                alco INTEGER NOT NULL,
                active INTEGER NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Criar tabela casos_historico
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS casos_historico (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                caso_dados TEXT NOT NULL,
                gabarito VARCHAR(50) NOT NULL,
                resposta_usuario VARCHAR(50) NOT NULL,
                acertou BOOLEAN NOT NULL,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("[OK] Tabelas de usuários e casos clínicos criadas com sucesso!")
        
    except Exception as e:
        print(f"[ERRO] Erro ao criar tabelas: {e}")

if __name__ == "__main__":
    create_database()