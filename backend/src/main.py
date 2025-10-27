from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .infrastructure.ml_model import ScikitLearnMLRepository
from .infrastructure.clinical_cases import InMemoryClinicalCaseRepository
from .application.use_cases import PredictRiskUseCase, GenerateClinicalCaseUseCase, AnalyzeVariableImpactUseCase
from .interfaces.controllers import CardiovascularController

def create_app() -> FastAPI:
    app = FastAPI(
        title="Sistema de Ensino Cardiovascular",
        description="API para ensino de doenças cardiovasculares com ML",
        version="1.0.0"
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Dependency Injection
    ml_repository = ScikitLearnMLRepository()
    case_repository = InMemoryClinicalCaseRepository()
    
    predict_use_case = PredictRiskUseCase(ml_repository)
    case_use_case = GenerateClinicalCaseUseCase(case_repository)
    study_use_case = AnalyzeVariableImpactUseCase(ml_repository)
    
    controller = CardiovascularController(predict_use_case, case_use_case, study_use_case)
    
    # Routes
    app.include_router(controller.router, prefix="/api/v1", tags=["cardiovascular"])
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)