from pydantic import BaseModel, EmailStr

from typing import List, Dict, Any


class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]
    recipients: List[str]


class EmailContent(BaseModel):
    subject: str
    html: str
