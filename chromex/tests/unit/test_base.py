import pytest
from asyncio import Future
from asyncio.coroutines import iscoroutinefunction
import tracemalloc
from base.abstract import BaseModel as _BaseModel
tracemalloc.start()

@pytest.fixture(scope="module")
def BaseModel():
    return _BaseModel

@pytest.fixture(scope="module")
def BaseModelClass(BaseModel):
    class BaseModelClass(BaseModel):
        pass
    return BaseModelClass



@pytest.mark.asyncio
async def test_base_model(BaseModel, BaseModelClass):
    assert issubclass(BaseModelClass, BaseModel)
    assert isinstance(BaseModelClass._tasks, list)
    assert iscoroutinefunction(BaseModelClass._run_sync)
    assert iscoroutinefunction(BaseModelClass.run_async)
    assert iscoroutinefunction(BaseModelClass.wait)
    assert iscoroutinefunction(BaseModelClass.close)
    assert iscoroutinefunction(BaseModelClass.__aenter__)
    assert iscoroutinefunction(BaseModelClass.__aexit__)
    assert iscoroutinefunction(BaseModelClass.__await__)



@pytest.mark.asyncio
async def test___aenter__(BaseModelClass):
    # Test __aenter__ method
    async with BaseModelClass() as model:
        assert model is not None


@pytest.mark.asyncio
async def test___aexit__(BaseModelClass):
    async with BaseModelClass() as model:
        assert model is not None
    try:
        assert model is None
    except NameError:
        pass

            
@pytest.mark.asyncio
async def test___await___(BaseModelClass):
    # Test __aenter__ method
    async with BaseModelClass() as model:
        assert isinstance(model, BaseModelClass)


@pytest.mark.asyncio
async def test_run_async(BaseModelClass):
    async with BaseModelClass() as model:
        def my_task():
            return 42
        task = model.run_async(my_task)
        assert task is Future
        task = await task
        assert task == 42


       
