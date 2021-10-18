from enum import Enum
from typing import Optional
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

import lib.db
import web.bindings

app = FastAPI()


class TitleClasses(str, Enum):
    freehold = "freehold"
    leasehold = "leasehold"


# ToDo: more detailed exception handling
@app.exception_handler(Exception)
async def basic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": f"Something went wrong: {exc}"},
    )


@app.get("/api/titles")
async def get_titles(title_class: Optional[TitleClasses] = None,
                     _sort: str = '',
                     _order: str = '',
                     _page: int = 1,
                     _limit: int = 10,
                     ):
    """ Search for titles.
        Returns:
        * title_id
        * title_number
        * title_class

        ToDo: append some metadata to response.
    """
    title_class_str = title_class.value if title_class is not None else ''
    return web.bindings.find_titles(title_class_str, _sort, _order, _page, _limit)


@app.get("/api/titles/{id}")
async def get_title_by_id(id: str):
    """
    Return all available fields of a given title id
    ToDo: append some metadata to response.
    """
    id_int = int(id)
    return web.bindings.find_title_by_id(id_int)


def main():
    lib.db.init()
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
