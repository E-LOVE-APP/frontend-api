from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect

from auth.security import authenticator

router = APIRouter(
    prefix="/chat",
)


@router.websocket(
    "/",
    # response_model=
    response={
        1000: {
            "description": "Message has been delivered successfully",
            # "model": MessageOutput,
        },
        1011: {
            "description": "Internal server error.",
            # "model": WebSocketInternalError,
        },
    },
    tags=["Messages", "Chat"],
    dependencies=[
        Depends(authenticator.authenticate),
    ],
)
async def create_wb_connection(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text({data})
    except WebSocketDisconnect:
        print("Client has been disconnected")
        await websocket.close(code=1000, reason="Normal closure")
