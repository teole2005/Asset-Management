from fastapi import APIRouter

# You already created the 'router' object here
router = APIRouter(prefix="/assets", tags=["Assets"])

# Use '@router', NOT '@app'
@router.get("/")
def list_assets():
    return [{"id": 1, "name": "Initial Asset"}]