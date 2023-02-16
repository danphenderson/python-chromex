from pydantic import Field, AnyHttpUrl, root_validator, UUID5
from uuid import uuid5, NAMESPACE_URL
from asyncio import Future
from chromex.abstract import BaseModel

class HRef(BaseModel):
    url: AnyHttpUrl
    id: UUID5 | None = Field(default=None) # sha1 hash of url for unique id
    
    @classmethod
    async def from_url(cls, url, *args, **kwargs) -> Future["HRef"]:
        async with cls(url=url, *args, **kwargs) as href:
            return href # type: ignore

    @root_validator
    def assign_id(cls, values: dict) -> dict:
        values["id"] = uuid5(NAMESPACE_URL, values["url"])
        return values

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.url == other
        elif isinstance(other, HRef):
            return self.url == other.url
        return False

    def __ne__(self, other) -> bool:
        return self.url != other.url

    def __str__(self) -> str:
        return str(self.url)

    async def __hash__(self):
        return hash(self.id)
        