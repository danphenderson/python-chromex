from abc import ABC
from asyncio import get_event_loop, ensure_future, Future, sleep
from pydantic import BaseModel as _BaseModel
from pydantic import Field

class BaseModel(ABC, _BaseModel):
    
    @staticmethod
    async def _run_sync(func, *args, **kwargs):
        loop = get_event_loop()
        return await loop.run_in_executor(None, func, *args, **kwargs)
    
    
    async def run_async(self, func, *args, **kwargs) -> Future:
        return await ensure_future(self._run_sync(func, *args, **kwargs))

    
    async def wait(self, seconds: int) -> None:
        if seconds > 0:
            await sleep(seconds)
            

    async def __aenter__(self):
        # Ref: https://peps.python.org/pep-0492/#asynchronous-context-managers-and-async-with
        return self

    
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        # Ref: https://peps.python.org/pep-0492/#asynchronous-context-managers-and-async-with 
        pass 
      

    async def __await__(self):
        return self._run_sync(lambda: self).__await__()
