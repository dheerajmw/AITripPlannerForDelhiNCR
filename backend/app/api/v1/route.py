"""Route optimization API."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.route import RouteOptimizeRequest, RouteOptimizeResponse
from app.services.route_service import RouteService

router = APIRouter(tags=["route"])


@router.post("/route/optimize", response_model=RouteOptimizeResponse)
async def optimize_route(
    body: RouteOptimizeRequest,
    db: Session = Depends(get_db),
) -> RouteOptimizeResponse:
    """Compute visit order and walking travel times between stops."""
    return RouteService(db).optimize(body)
