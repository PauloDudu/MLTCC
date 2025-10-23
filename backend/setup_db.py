"""
Script para configurar o banco de dados PostgreSQL
"""
import subprocess
import sys

def run_command(command, description):
    print(f"\n[INFO] {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[OK] {description} - Concluído")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERRO] {description} - Falhou")
        if e.stderr:
            print(e.stderr)
        return False

def main():
    print("=== Configuração do Banco PostgreSQL ===")
    
    # 1. Criar banco
    if not run_command("python create_database.py", "Criando banco de dados"):
        return
    
    # 2. Executar migrations
    if not run_command("alembic upgrade head", "Aplicando migrations"):
        return
    
    print("\n[OK] Banco PostgreSQL configurado com sucesso!")
    print("Banco: cardio_ml_db")
    print("Host: localhost:5432")
    print("User: postgres")

if __name__ == "__main__":
    main()