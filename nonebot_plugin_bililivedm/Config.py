from pydantic import BaseModel

class Config(BaseModel):
    bililivedown:str ="on"
    bililiveid: list = []
    bilitoken :str = ""
    loadws :str = "ws://127.0.0.1:8000/bilidm"