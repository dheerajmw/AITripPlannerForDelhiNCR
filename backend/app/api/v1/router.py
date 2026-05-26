"""Aggregate API v1 routes."""

from fastapi import APIRouter

from app.api.v1 import health, itinerary, pois, route

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(pois.router)
api_router.include_router(route.router)
api_router.include_router(itinerary.router)
