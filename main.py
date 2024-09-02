import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from alembic import command
from alembic.config import Config
from logging.config import fileConfig
from domain.answer import answer_router
from domain.question import question_router

# Alembic 설정
def run_migrations() -> None:
    # Alembic Config object
    alembic_cfg = Config("alembic.ini")

    # 환경 변수에서 DATABASE_URL을 가져옵니다
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        alembic_cfg.set_main_option("sqlalchemy.url", database_url)

    # 로깅 설정
    if alembic_cfg.config_file_name is not None:
        fileConfig(alembic_cfg.config_file_name)

    # Alembic 마이그레이션 실행
    command.upgrade(alembic_cfg, "head")

# FastAPI 앱 생성
app = FastAPI()

# CORS 설정
origins = [
    "http://127.0.0.1:5173", 
    "http://localhost:5173", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 추가
app.include_router(question_router.router)
app.include_router(answer_router.router)

# 헬스체크 엔드포인트
@app.get("/api/health")
async def health_check():
    return PlainTextResponse("건강합니다", status_code=200)

# 애플리케이션 시작 시 Alembic 마이그레이션 실행
@app.on_event("startup")
async def on_startup():
    run_migrations()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# import os
# from fastapi import FastAPI
# from starlette.middleware.cors import CORSMiddleware
# from fastapi.responses import PlainTextResponse
# from alembic import command
# from alembic.config import Config
# from logging.config import fileConfig
# from domain.answer import answer_router
# from domain.question import question_router

# # Alembic 설정
# def run_migrations() -> None:
#     # Alembic Config object
#     alembic_cfg = Config("alembic.ini")

#     # 환경 변수에서 DATABASE_URL을 가져옵니다
#     database_url = os.getenv("DATABASE_URL")
#     if database_url:
#         alembic_cfg.set_main_option("sqlalchemy.url", database_url)

#     # 로깅 설정
#     if alembic_cfg.config_file_name is not None:
#         fileConfig(alembic_cfg.config_file_name)

#     # Alembic 마이그레이션 실행
#     command.upgrade(alembic_cfg, "head")

# # FastAPI 앱 생성
# app = FastAPI()

# # 애플리케이션 시작 시 Alembic 마이그레이션 실행
# run_migrations()

# # CORS 설정
# origins = [
#     "http://127.0.0.1:5173", 
#     "http://localhost:5173", 
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # 라우터 추가
# app.include_router(question_router.router)
# app.include_router(answer_router.router)

# # 헬스체크 엔드포인트
# @app.get("/api/health")
# async def health_check():
#     return PlainTextResponse("건강합니다", status_code=200)
