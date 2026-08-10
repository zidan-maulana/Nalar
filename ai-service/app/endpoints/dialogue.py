from fastapi import APIRouter, status
from app.schemas.dialogue import DialogueTurnRequest, DialogueTurnResponse
from app.agents.dialogue_loop_agent import process_dialogue_turn

router = APIRouter(prefix="/dialogue", tags=["Stage 3: Adaptive Dialogue Engine"])

@router.post("/turn", response_model=DialogueTurnResponse, status_code=status.HTTP_200_OK)
async def dialogue_turn(request: DialogueTurnRequest):
    """
    Endpoint Stage 3: Memproses 1 turn interogasi adaptif (LoopAgent).
    Menilai jawaban pengguna terhadap Master Rubric, memutuskan drill-down atau naik level,
    serta mengekstrak evidence trail.
    """
    return process_dialogue_turn(request)
