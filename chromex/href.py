from pydantic import BaseModel, Field, AnyHttpUrl, root_validator, UUID5
from uuid import uuid5, NAMESPACE_URL
from asyncio import get_event_loop, ensure_future, Future, gather

class HRef(BaseModel):
    url: AnyHttpUrl
    is_static: bool = Field(default=False)
    id: UUID5 | None = Field(default=None) # sha1 hash of url for unique id
    _tasks: list[Future] = Field(default_factory=list)

    @staticmethod
    async def _run_sync(func):
        loop = get_event_loop()
        return await loop.run_in_executor(None, func)
    
    @classmethod
    async def from_url(cls, url, *args, **kwargs) -> "HRef":
        async with cls(url=url, *args, **kwargs) as href:
            return href

    async def run_async(self, func):
        task = ensure_future(self._run_sync(func))
        self._tasks.append(task)
        return await task

    @root_validator
    def assign_id(cls, values):
        values["id"] = uuid5(NAMESPACE_URL, values["url"])
        return values

    def __eq__(self, other):
        if isinstance(other, str):
            return self.url == other
        elif isinstance(other, HRef):
            return self.url == other.url
        return False

    def __ne__(self, other):
        return self.url != other.url

    def __str__(self) -> str:
        return str(self.url)

    async def __aenter__(self):
        return self

    async def __hash__(self):
        return hash(self.id)

    async def __await__(self):
        return self._run_sync(lambda: self).__await__()

    async def __aexit__(self, exc_type, exc_value, traceback):
        
        if self._tasks:
            await gather(*self._tasks)
        return None