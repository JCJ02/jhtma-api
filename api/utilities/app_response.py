from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, Union, Dict, List
from api.configurations.configuration import configuration

class AppResponse:
    @staticmethod
    def send_successful(
            *,
            data: Union[Dict, List, None] = None,
            message: str = "",
            code: int = 200,
    ) -> JSONResponse:
        response_content = {
            "status": "success",
            "message": message,
            "data": jsonable_encoder(data),
            "code": code
        }
        return JSONResponse(content=response_content, status_code=code)
    
    @staticmethod
    def send_error(
            *,
            data: Union[Dict, List, None] = None,
            message: str,
            code: int,
    ) -> JSONResponse:
        
        project_env = configuration["app"]["env"]

        response_message = (
            "Internal Server Error" if project_env != "development" and code == 500 else message
        )
        
        response_content = {
            "status": "error",
            "message": response_message,
            "data": jsonable_encoder(data),
            "code": code
        }
        return JSONResponse(content=response_content, status_code=code)