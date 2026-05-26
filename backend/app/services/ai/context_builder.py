"""Build Groq context from draft itinerary and capped POI shortlist."""

from typing import Any, Dict, List, Sequence

from app.config import AI_CONTEXT_POI_CAP
from app.db.models import POIRecord
from app.models.itinerary import ItineraryGenerateRequest, ItineraryResponse


class ContextBuilder:
    @staticmethod
    def build(
        request: ItineraryGenerateRequest,
        draft: ItineraryResponse,
        candidate_pois: Sequence[POIRecord],
    ) -> Dict[str, Any]:
        draft_ids = {s.poi_id for s in draft.stops}
        capped: List[POIRecord] = []
        seen = set()

        for poi in sorted(candidate_pois, key=lambda p: p.id):
            if poi.id in seen:
                continue
            seen.add(poi.id)
            capped.append(poi)
            if len(capped) >= AI_CONTEXT_POI_CAP:
                break

        for stop in draft.stops:
            if stop.poi_id not in seen and len(capped) < AI_CONTEXT_POI_CAP:
                seen.add(stop.poi_id)
                capped.append(
                    POIRecord(
                        id=stop.poi_id,
                        name=stop.name,
                        category=stop.category,
                        lat=0.0,
                        lon=0.0,
                        estimated_visit_minutes=stop.visit_minutes,
                        source="draft",
                    )
                )

        allowed_ids = sorted(draft_ids | {p.id for p in capped})

        return {
            "preferences": {
                "budget": request.budget,
                "interests": list(request.interests),
                "duration": request.duration,
                "duration_minutes": request.duration_minutes,
            },
            "allowed_poi_ids": allowed_ids,
            "candidate_pois": [
                {
                    "poi_id": p.id,
                    "name": p.name,
                    "category": p.category,
                    "tags": p.get_tags_list() if hasattr(p, "get_tags_list") else [],
                    "estimated_visit_minutes": p.estimated_visit_minutes,
                    "opening_hours": p.opening_hours,
                }
                for p in capped
            ],
            "draft_itinerary": {
                "stops": [
                    {
                        "order": s.order,
                        "poi_id": s.poi_id,
                        "name": s.name,
                        "category": s.category,
                        "arrive_at": s.arrive_at,
                        "depart_at": s.depart_at,
                        "visit_minutes": s.visit_minutes,
                    }
                    for s in draft.stops
                ]
            },
        }
