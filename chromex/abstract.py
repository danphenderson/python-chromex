from abc import ABC
from asyncio import get_event_loop, ensure_future, Future, gather, sleep
from pydantic import BaseModel as _BaseModel

class BaseModel(_BaseModel, ABC):
    _tasks: list[Future] = []
    
    
    @staticmethod
    async def _run_sync(func, *args):
        loop = get_event_loop()
        return await loop.run_in_executor(None, func, *args)
    

    @classmethod
    async def run_async(cls, func, *args):
        task = ensure_future(cls._run_sync(func, *args))
        cls._tasks.append(task)
        return await task

    async def wait(self, seconds: int) -> None:
        await self.run_async(sleep, seconds)

    
    async def close(self) -> None:
        if self._tasks:
            await gather(*self._tasks)
        

    async def __aenter__(self):
        # Ref: https://peps.python.org/pep-0492/#asynchronous-context-managers-and-async-with
        return self

    
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        # Ref: https://peps.python.org/pep-0492/#asynchronous-context-managers-and-async-with 
        await self.close()
      

    async def __await__(self, *args):
        return self._run_sync(lambda: self, *args).__await__()
