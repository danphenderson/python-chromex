from asyncio import Future
from pydantic import Field, AnyHttpUrl, root_validator, UUID5
from uuid import uuid5, NAMESPACE_URL
from Levenshtein import ratio as levenstien_norm
from Levenshtein import distance as levenstien_dist
from chromex.base.abstract import BaseModel

class HRef(BaseModel):
    url: AnyHttpUrl
    id: UUID5 | None = Field(default=None) # sha1 hash of url for unique id
    
    @classmethod
    async def from_url(cls, url) -> "HRef":
        async with cls(url=url) as href:
            return href

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

    @property
    def scheme(self) -> str:
        return self.url.scheme

    @property
    def host(self) -> str:
        return self.url.host or ''
     
    @property
    def host_type(self) -> str:
        return self.url.host_type

    @property
    def path(self) -> str:
        return self.url.path or ''
        
    @property
    def query(self) -> str:
        return self.url.query or ''

    async def levenstien_norm(self, href:"HRef") -> Future[float]:
        """Calculate the distance between two HRefs"""

        return await self.run_async(lambda: levenstien_norm(self.url, href.url))

    async def levenstien_dist(self, href:"HRef") -> Future[int]:
        """Calculate the distance between two HRefs"""
        return await self.run_async(lambda: levenstien_dist(self.url, href.url) * len(self.url))


async def href(url: str) -> HRef:
    return await HRef.from_url(url)