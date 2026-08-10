from app.config import settings
from app.schemas.score import ScoreRequest, ScoreResponse

def calculate_score(request: ScoreRequest) -> ScoreResponse:
    """
    Menghitung Raw Depth Score, Normalisasi Confidence, Delta, dan Calibration Status.
    
    Formula:
    1. Base Points:
       - Definisi = SCORE_DEFINISI (default: 40.0)
       - Sebab-Akibat = SCORE_SEBAB_AKIBAT (default: 70.0)
       - Transfer = SCORE_TRANSFER (default: 100.0)
    2. Penalti: -5.0 per extra round jika rounds_used > 1
    3. Depth Score = clamp(Base Points - Penalti, 0, 100)
    4. Confidence Normalized = (confidence_input - 1) / 4 * 100
    5. Delta = Confidence Normalized - Depth Score
    6. Calibration Status:
       - Delta > CALIBRATION_THRESHOLD (+15.0) -> overconfident
       - Delta < -CALIBRATION_THRESHOLD (-15.0) -> underconfident
       - else -> accurate
    """
    # 1. Base Points
    if request.level_reached == "definisi":
        base_score = settings.SCORE_DEFINISI
    elif request.level_reached == "sebab-akibat":
        base_score = settings.SCORE_SEBAB_AKIBAT
    elif request.level_reached == "transfer":
        base_score = settings.SCORE_TRANSFER
    else:
        base_score = 0.0

    # 2. Penalti Extra Rounds
    extra_rounds = max(0, request.rounds_used - 1)
    penalty = extra_rounds * settings.PENALTY_EXTRA_ROUND

    # 3. Final Depth Score
    raw_depth = base_score - penalty
    depth_score = round(max(0.0, min(100.0, raw_depth)), 2)

    # 4. Confidence Normalization (Skala 1-5 -> 0-100)
    confidence_normalized = round(((request.confidence_input - 1) / 4.0) * 100.0, 2)

    # 5. Delta Calculation
    delta = round(confidence_normalized - depth_score, 2)

    # 6. Status Calibration & Narasi Summary
    threshold = settings.CALIBRATION_THRESHOLD

    if delta > threshold:
        calibration_status = "overconfident"
        summary_reason = (
            f"Pengguna merasa sangat yakin ({request.confidence_input}/5 = {confidence_normalized:.0f}%), "
            f"namun pemahaman aktual baru mencapai level '{request.level_reached.capitalize()}' ({depth_score:.0f}%). "
            f"Ini berpotensi berbahaya karena pengguna tidak sadar perlu belajar lagi."
        )
    elif delta < -threshold:
        calibration_status = "underconfident"
        summary_reason = (
            f"Pengguna merasa kurang yakin ({request.confidence_input}/5 = {confidence_normalized:.0f}%), "
            f"padahal pemahamannya sudah mencapai level '{request.level_reached.capitalize()}' ({depth_score:.0f}%). "
            f"Pengguna perlu lebih percaya diri dengan pemahamannya."
        )
    else:
        calibration_status = "accurate"
        summary_reason = (
            f"Penilaian diri pengguna ({request.confidence_input}/5 = {confidence_normalized:.0f}%) sangat akurat "
            f"dan sejalan dengan pemahaman aktual di level '{request.level_reached.capitalize()}' ({depth_score:.0f}%)."
        )

    return ScoreResponse(
        session_id=request.session_id,
        concept_id=request.concept_id,
        depth_score=depth_score,
        confidence_input=request.confidence_input,
        confidence_normalized=confidence_normalized,
        delta=delta,
        calibration_status=calibration_status,
        summary_reason=summary_reason
    )
