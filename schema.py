from pydantic import BaseModel, ValidationError

from errors import HttpError

class CreateUser(BaseModel):
    name: str
    password: str

class UpdateUser(BaseModel):
    name: str | None = None
    password: str | None = None

class CreateAdvertisement(BaseModel):
    title: str
    description: str
    owner_id: int

class UpdateAdvertisement(BaseModel):
    title: str | None = None
    description: str | None = None
    owner_id: int | None = None

def validate(json_data: dict, schema_cls: type[BaseModel]) -> dict:
    try:
        return schema_cls(**json_data).model_dump(exclude_unset=True)
    except ValidationError as err:
        errors = err.errors()
        for e in errors:
            e.pop("ctx", None)
        raise HttpError(errors, 400)