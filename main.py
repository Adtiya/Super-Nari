from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.run_agent import router as agent_router
from routes.run_script import router as script_runner
from routes.runtime_check import router as runtime_checker
from routes.export_agent import router as export_router
from routes.memory import router as memory_router
from routes.asi import router as asi_router
from routes.self_heal import router as self_heal_router
from routes.templates_router_sample import router as templates_router
from routes.run_agent_with_memory_final import router as agent_router
from routes.consciousness_routes import router as memory_ai_router



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(templates_router, prefix="/templates")
app.include_router(agent_router, prefix="/agent")
app.include_router(script_runner, prefix="/agent")
app.include_router(runtime_checker, prefix="/runtime")
app.include_router(export_router, prefix="/agent")
app.include_router(memory_router, prefix="/memory")  # ⬅️ THIS now handles /view and /annotate
app.include_router(asi_router, prefix="/asi")
app.include_router(self_heal_router, prefix="/agent")
app.include_router(memory_ai_router, prefix="/memory_ai")