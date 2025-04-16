from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.responses.responses import error_response
from src.routers.user_router import user_router


api = FastAPI()


@api.middleware('http')
async def http_error_handler(request: Request, call_next) -> Response | JSONResponse:
    try:
        print('Middleware Running!')
        return await call_next(request)
    except RequestValidationError as e:
        raise e
    except IntegrityError as e:
        raise e
    except SQLAlchemyError as e:
        raise e
    except HTTPException as e:
        raise e
    except Exception as e:
        message = f'Exception: {str(e)}'
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return error_response(message=message, status_code=status_code)


@api.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return error_response(
        status_code=422,
        message=f"RequestValidation failed, wrong format or missing data {exc.errors()}"
    )


@api.exception_handler(IntegrityError)
async def handle_integrity_error(request: Request, exc: IntegrityError):
    return error_response(
        status_code=409,
        message="User with this ID or username already exists."
    )


@api.exception_handler(SQLAlchemyError)
async def handle_sqlalchemy_error(request: Request, exc: SQLAlchemyError):
    return error_response(
        status_code=500,
        message=f"Database Error occurred while processing the request. {exc}"
    )


@api.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return error_response(
        status_code=exc.status_code,
        message=exc.detail
    )


@api.get('/', tags=['Home'])
def home():
    return PlainTextResponse(content='Home', status_code=200)


api.include_router(prefix='/users', router=user_router)


