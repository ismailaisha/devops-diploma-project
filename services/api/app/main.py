from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api import auth, exercises, programs, schedules, attendance, health

# Создаём все таблицы в БД при старте
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FitFlow API",
    description="SaaS платформа для управления фитнес-тренировками",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS — разрешаем запросы с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router,       prefix="/api/auth",       tags=["Auth"])
app.include_router(exercises.router,  prefix="/api/exercises",  tags=["Exercises"])
app.include_router(programs.router,   prefix="/api/programs",   tags=["Programs"])
app.include_router(schedules.router,  prefix="/api/schedules",  tags=["Schedules"])
app.include_router(attendance.router, prefix="/api/attendance", tags=["Attendance"])