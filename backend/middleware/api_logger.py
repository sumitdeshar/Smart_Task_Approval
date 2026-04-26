# import time
# import asyncio
# from datetime import datetime
# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.requests import Request

# from configs.db import async_session
# from models.user_model import APILog
# from utils.session_manager import get_active_session_id

# SKIP_PATHS = {"/docs", "/openapi.json", "/redoc", "/favicon.ico", "/auth/login", "/auth/register"}

# class APILoggerMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         if request.url.path in SKIP_PATHS:
#             return await call_next(request)

#         start    = time.monotonic()
#         response = await call_next(request)
#         elapsed  = int((time.monotonic() - start) * 1000)

#         # fire-and-forget — never delays the response
#         asyncio.create_task(self._write_log(
#             user_id    = getattr(request.state, "user_id", None),
#             method     = request.method,
#             path       = request.url.path,
#             status_code= response.status_code,
#             duration_ms= elapsed,
#         ))
#         return response

#     async def _write_log(self, user_id, method, path, status_code, duration_ms):
#         async with async_session() as db:
#             session_id = None
#             if user_id:
#                 session_id = await get_active_session_id(db, user_id)

#             db.add(APILog(
#                 user_id    = user_id,
#                 session_id = session_id,
#                 method     = method,
#                 path       = path,
#                 status_code= status_code,
#                 duration_ms= duration_ms,
#                 timestamp  = datetime.utcnow(),
#             ))
#             await db.commit()