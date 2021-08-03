from fastapi import FastAPI

# from starlette.middleware.cors import CORSMiddleware
# TODO
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
from app.core import config, tasks


def get_application():
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)
    """ 
    This is a factory functions which returns FastAppi app with cors middleware configured 
    About cors You can read more here: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
    """

    # TODO read about middleware and all allows things below
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # register event handlers for db
    app.add_event_handler(
        "startup", tasks.create_start_app_handlers(app)
    )  # 'startup' means that this handler will be executed when the application starts
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    app.include_router(api_router, prefix="/api")

    return app


app = get_application()
