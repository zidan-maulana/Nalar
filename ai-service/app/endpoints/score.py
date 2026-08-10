from fastapi import APIRouter, status
from app.schemas.score import ScoreRequest, ScoreResponse
from app.services.scoring import calculate_score

router = APIRouter(prefix="/score", tags=["Stage 4: Scoring & Confidence Calibration"])

@router.post("", response_model=ScoreResponse, status_code=status.HTTP_200_OK)
async def score_concept(request: ScoreRequest):
    """
    Endpoint Stage 4: Menghitung Depth Score & Confidence Calibration.
    Fungsi logika murni matematika, deterministik, dan bebas dari ketergantungan LLM.
    """
    return calculate_score(request)
