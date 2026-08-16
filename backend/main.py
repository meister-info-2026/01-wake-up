import os
import sys

# ==============================================================================
# sys.path 자동 경로 주입 (어느 디렉토리에서 실행하든 절대/상대 경로 임포트 오류 방지)
# ==============================================================================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from websocket_manager import ws_manager

app = FastAPI(
    title="Smart IoT & Vision Control System API",
    version="1.0.0",
    description="IoT 센서 및 액추에이터 제어, 영상인식 트리거 백엔드 API"
)

# CORS 설정 (Next.js 로컬 개발 및 클라우드 배포 지원)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """백엔드 서버 헬스체크 엔드포인트"""
    return {"status": "ok", "message": "Backend server is running healthy."}


@app.get("/")
async def root():
    """루트 안내 엔드포인트"""
    return {
        "message": "Smart IoT & Vision Control Backend is active.",
        "docs_url": "/docs",
        "health_url": "/health"
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """실시간 디바이스 상태 스트리밍용 WebSocket 엔드포인트"""
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # 클라이언트로부터 수신된 메시지 처리 (필요 시)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        ws_manager.disconnect(websocket)
