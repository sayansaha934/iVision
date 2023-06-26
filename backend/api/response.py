
from fastapi.responses import JSONResponse

class ApiResponse:

    @staticmethod
    def response_ok(
        message="Ok",
        code=200,
        success=True,
        data={},

    ):
        data = {
            "message": message,
            "status_code": code,
            "success": success,
            "data": data,
        }
        return JSONResponse(content=data, status_code=code)

    @staticmethod
    def response_internal_server_error(
        message="Internal server error",
        code=500,
        success=False,
        data={},
        e='',
    ):
        message = str(e)
        data = {
            "message": message,
            "status_code": code,
            "success": success,
            "data": data,
        }

        return JSONResponse(content=data, status_code=code)

    @staticmethod
    def response_bad_request(
        message="Bad Request",
        code=400,
        success=False,
        data={},
    ):
        data = {
            "message": message,
            "status_code": code,
            "success": success,
            "data": data,
        }
        return JSONResponse(content=data, status_code=code)



