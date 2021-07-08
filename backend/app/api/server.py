from fastapi import FastAPI
#from starlette.middleware.cors import CORSMiddleware
#TODO
""" 
About starlette
FastAPI is built on top of starlette more info https://www.starlette.io/
"""

from fastapi.middleware.cors import CORSMiddleware
"""
But developers from FastAPI created the interface for the most of the starlette interface
so we can import it directly from fastapi
"""

from app.api.routes import router as api_router


def get_application():


    app = FastAPI(title="Phresh", version="1.0.0")
    """ 
    This is a factory functions which returns FastAppi app with cors middleware configured 
    About cors You can read more here: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
    """

    #TODO read about middleware and all allows things below
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(api_router, prefix="/api")

    return app

app = get_application()