import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

def load_cardiovascular_dataset():
    """Carrega o dataset real de doenças cardiovasculares"""
    # Caminho para o dataset
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'cardio_train.csv')
    
    if not os.path.exists(csv_path):
        print(f"Dataset não encontrado em: {csv_path}")
        return create_sample_dataset()
    
    # Carregar dataset
    df = pd.read_csv(csv_path, sep=';')
    
    # Converter idade de dias para anos
    df['age'] = (df['age'] / 365.25).astype(int)
    
    # Usar todo o dataset (70k amostras)
    print(f"Dataset completo carregado: {len(df)} amostras")
    
    # Remover outliers extremos
    df = df[
        (df['ap_hi'] >= 70) & (df['ap_hi'] <= 300) &
        (df['ap_lo'] >= 40) & (df['ap_lo'] <= 200) &
        (df['height'] >= 100) & (df['height'] <= 250) &
        (df['weight'] >= 30) & (df['weight'] <= 200)
    ]
    
    return df

def create_sample_dataset():
    """Cria um dataset sintético caso o real não esteja disponível"""
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'age': np.random.randint(30, 80, n_samples),
        'gender': np.random.randint(1, 3, n_samples),
        'height': np.random.randint(150, 190, n_samples),
        'weight': np.random.randint(50, 100, n_samples),
        'ap_hi': np.random.randint(90, 180, n_samples),
        'ap_lo': np.random.randint(60, 120, n_samples),
        'cholesterol': np.random.randint(1, 4, n_samples),
        'gluc': np.random.randint(1, 4, n_samples),
        'smoke': np.random.randint(0, 2, n_samples),
        'alco': np.random.randint(0, 2, n_samples),
        'active': np.random.randint(0, 2, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Criar target baseado em regras médicas
    df['cardio'] = 0
    df.loc[(df['age'] > 60) | (df['cholesterol'] > 2) | (df['ap_hi'] > 140), 'cardio'] = 1
    df.loc[(df['age'] > 70) & (df['cholesterol'] == 3), 'cardio'] = 1
    
    return df

def train_model():
    # Carregar dataset real
    df = load_cardiovascular_dataset()
    print(f"Dataset carregado com {len(df)} amostras")
    
    # Separar features e target
    feature_columns = ['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 
                      'cholesterol', 'gluc', 'smoke', 'alco', 'active']
    X = df[feature_columns]
    y = df['cardio']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Treinar modelo
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Avaliar
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Acurácia: {accuracy:.3f}")
    print("\nRelatório de classificação:")
    print(classification_report(y_test, y_pred))
    
    # Salvar modelo
    joblib.dump(model, 'cardiovascular_model.pkl')
    print("\nModelo salvo como 'cardiovascular_model.pkl'")
    
    return model

if __name__ == "__main__":
    train_model()