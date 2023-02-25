from chromex.base.abstract import BaseModel

class HPage(BaseModel):
    title : str = ""
    source : str = ""

async def hpage(title: str, source: str) -> HPage:
    async with HPage(title=title, source=source) as hpage:
        return hpage