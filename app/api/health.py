from fastapi import APIRouter

router = APIRouter(prefix="/market", tags=["market"])

@router.get('/health')
def health():
    if router:
        return {
            "status": "connected"
        }
    else:
        return {
            "status": "fastapi connection failed "
        }
    
