# 🏗️ Arquitetura do Sistema

## 📐 Clean Architecture

O projeto segue os princípios da **Clean Architecture**, garantindo separação de responsabilidades e facilidade de manutenção.

### **Camadas da Arquitetura**

```
┌─────────────────────────────────────┐
│            Interfaces               │  ← Controllers, DTOs, API
├─────────────────────────────────────┤
│           Application               │  ← Use Cases, Orquestração
├─────────────────────────────────────┤
│            Domain                   │  ← Entidades, Regras de Negócio
├─────────────────────────────────────┤
│         Infrastructure              │  ← ML Models, Repositórios
└─────────────────────────────────────┘
```

## 🔧 Backend (FastAPI)

### **Domain Layer**
- `entities.py`: Entidades de negócio (PatientData, RiskPrediction)
- Regras de negócio puras, sem dependências externas

### **Application Layer**
- `use_cases.py`: Casos de uso (PredictRisk, GenerateCase)
- Orquestração da lógica de negócio

### **Infrastructure Layer**
- `ml_model.py`: Implementação do modelo ML
- `clinical_cases.py`: Repositório de casos clínicos
- Implementações concretas dos repositórios

### **Interfaces Layer**
- `controllers.py`: Controllers FastAPI
- `dtos.py`: Data Transfer Objects
- Adaptadores para comunicação externa

## 🎨 Frontend (Vue.js + Vuetify)

### **Estrutura de Componentes**
```
src/
├── views/           # Páginas principais
│   ├── Home.vue
│   ├── Predict.vue
│   └── ClinicalCases.vue
├── components/      # Componentes reutilizáveis
├── services/        # Comunicação com API
├── router/          # Roteamento
└── plugins/         # Configurações (Vuetify)
```

### **Tecnologias Frontend**
- **Vue.js 3**: Framework reativo
- **Vuetify**: Material Design
- **Vue Router**: Roteamento SPA
- **Axios**: Cliente HTTP
- **SweetAlert2**: Notificações elegantes

## 🤖 Machine Learning

### **Pipeline ML**
1. **Dataset Sintético**: Geração de dados realistas
2. **Treinamento**: RandomForest com 98.5% acurácia
3. **Predição**: Classificação de risco (Baixo/Médio/Alto)
4. **Análise**: Impacto de variáveis em tempo real

### **Features Utilizadas**
- Idade, Sexo, Tipo de dor no peito
- Pressão arterial, Colesterol, Glicemia
- ECG, Frequência cardíaca máxima
- Angina por exercício, Depressão ST

## 🔄 Fluxo de Dados

```
Frontend → API → Use Case → ML Model → Response → Frontend
    ↓         ↓        ↓         ↓          ↓         ↓
  Vue.js → FastAPI → Domain → sklearn → JSON → SweetAlert
```

## 🐳 Containerização

### **Docker Compose**
- **Backend**: Python + FastAPI
- **Frontend**: Node.js + Vue.js
- **Database**: PostgreSQL (opcional)
- **Volumes**: Persistência de dados

## 🔒 Princípios Aplicados

1. **Dependency Inversion**: Interfaces abstratas
2. **Single Responsibility**: Uma responsabilidade por classe
3. **Open/Closed**: Extensível sem modificação
4. **Separation of Concerns**: Camadas bem definidas
5. **SOLID Principles**: Código limpo e manutenível