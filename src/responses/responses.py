from fastapi.responses import JSONResponse


def success_response(data={}, message='Success', status_code=200):
    return JSONResponse(
        status_code=status_code,
        content={
            'success': True,
            'data': data,
            'message': message
        }
    )


def error_response(message='Error', status_code=400):
    return JSONResponse(
        status_code=status_code,
        content={
            'success': False,
            'data': None,
            'message': message
        }
    )
