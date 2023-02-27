from abc import ABCMeta
from asyncio import get_event_loop, ensure_future, Future, sleep, gather
from inspect import iscoroutine
from pydantic import BaseModel as _BaseModel
from pydantic import Field

class BaseModel(_BaseModel, metaclass=ABCMeta):
    _tasks: list = []

    @staticmethod
    async def _run_sync(func, *args, **kwargs):
        loop = get_event_loop()
        return await loop.run_in_executor(None, func, *args, **kwargs)
    
    
    async def run_async(self, func, *args, **kwargs) -> Future:
        task = ensure_future(self._run_sync(func, *args, **kwargs))
        self._tasks.append(task)
        return await task
    

    async def wait(self, seconds: int) -> None:
        if seconds > 0:
            await sleep(seconds)
            

    async def __aenter__(self):
        # Ref: https://peps.python.org/pep-0492/#asynchronous-context-managers-and-async-with
        return self


    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        # Ref: https://peps.python.org/pep-0492/#asynchronous-context-managers-and-async-with 
        coroutines = []
        if self._tasks:
            for task in self._tasks:
                if iscoroutine(task):
                    coroutines.append(task)
                else:
                    # handle non-coroutine objects here, if necessary
                    pass
            await gather(*coroutines)
          
    async def __await__(self):
        return self._run_sync(lambda: self).__await__()
