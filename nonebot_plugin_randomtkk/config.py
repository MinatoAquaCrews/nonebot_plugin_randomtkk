from pydantic import BaseModel, Extra
from pathlib import Path
from nonebot import logger
import nonebot
import httpx
import aiofiles

class RandomTkkConfig(BaseModel, extra=Extra.ignore):
    
    tkk_path: Path = Path(__file__).parent / "resource"
    easy_size: int = 10
    normal_size: int = 20
    hard_size: int = 40
    extreme_size: int = 60
    max_size: int = 80
    show_coordinate: bool = True
    
driver = nonebot.get_driver()
tkk_config: RandomTkkConfig = RandomTkkConfig.parse_obj(driver.config.dict())
TKK_PATH: Path = tkk_config.tkk_path

characters = {
    "honoka": "穗乃果",
    "eli": "绘理",
    "umi": ["海未"],
    "maki": ["西木野真姬", "真姬"],
    "rin": ["星空凛", "凛"],
    "hanayo": ["花阳"],
    "nico": ["妮可"],
    "nozomi": ["东条希"],
    "kotori": ["南小鸟"],
    "you": ["渡边曜"],
    "dia": ["黑泽黛雅"],
    "riko": ["樱内梨子"],
    "yoshiko": ["津岛善子"],
    "ruby": ["黑泽露比"],
    "hanamaru": ["国木田花丸"],
    "mari": ["小原鞠莉"],
    "kanan": ["松浦果南"],
    "chika": ["高海千歌"],
    "ren": ["叶月恋"],
    "sumire": ["平安名堇"],
    "chisato": ["岚千砂都"],
    "kanon": ["涩谷香音"],
    "tankuku": ["唐可可"]
}

class DownloadError(Exception):
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return self.msg

async def download_url(url: str) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                response = await client.get(url)
                if response.status_code != 200:
                    continue
                return response
            except Exception as e:
                logger.warning(f"Error occured when downloading {url}, {i+1}/3: {e}")
    
    raise DownloadError("Resource of Tankuku plugin missing! Please check!")

@driver.on_startup
async def _():
    tkk_path: Path = tkk_config.tkk_path
    
    if not tkk_path.exists():
        tkk_path.mkdir(parents=True, exist_ok=True)
        
    url = "https://raw.fastgit.org/MinatoAquaCrews/nonebot_plugin_randomtkk/main/nonebot_plugin_randomtkk/resource/"
    
    for chara in characters:
        _name = chara + ".png"
        if not (tkk_path / _name).exists():
            response = await download_url(url + _name)
            await save_resource(_name, response)

    if not (tkk_path / "mark.png").exists():
        response = await download_url(url + "mark.png")
        await save_resource("mark.png", response)
        
    if not (tkk_path / "msyh.ttc").exists():
        response = await download_url(url + "msyh.ttc")
        await save_resource("msyh.ttc", response)

async def save_resource(name: str, response: httpx.Response) -> None:
    async with aiofiles.open((tkk_config.tkk_path / name), "wb") as f:
        await f.write(response.content)