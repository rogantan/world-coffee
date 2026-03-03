from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime, timedelta
from typing import Optional
from app.admin.enum.status import Status

class SyncShema(BaseModel):
    start_time: datetime
    finish_time: datetime | None
    status: str
    color: Optional[str] = None

    @field_validator("start_time", "finish_time", mode="before")
    @classmethod
    def format_datetime(cls, v):
        if v:
            return v + timedelta(hours=3)
        
    @model_validator(mode="after")
    def set_color(self):
        if self.status == Status.SUCCESS.value:
            self.color = "green"
        elif self.status == Status.IN_PROGRESS.value:
            self.color = "yellow"
        elif self.status == Status.ERROR.value:
            self.color = "red"
        return self