from fastapi import APIRouter, HTTPException, Request, UploadFile
from RTN import parse
from PTT import parse_title

router = APIRouter(
    prefix="",
    tags=["default"],
)


@router.get(
        "/",
        summary="Root endpoint",
        description="This endpoint is the root of the API. It is used to check if the API is running.",
        include_in_schema=False,
)
async def read_root():
    return {"message": "Welcome to Thresh!"}


@router.post("/parse")
async def parse_post(request: Request, filename: str, raw: bool = False):
    """
    Parse a file and return the parsed content.
    """
    return parse_title(filename) if raw else parse(filename, translate_langs=True)
