from fastapi import APIRouter

from routes import user, pet, species

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(pet.router, prefix="/pets", tags=["Pets"])
api_router.include_router(species.router, prefix="/species", tags=["Species"])
