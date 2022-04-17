from pydantic import BaseModel, Extra
from pathlib import Path
import os
import nonebot

class RandomTkkConfig(BaseModel, extra=Extra.ignore):
    
    tkk_path: str = os.path.join(os.path.dirname(__file__), "resource")
    easy_size:  int = 10
    normal_size: int = 20
    hard_size: int = 30
    extreme_size: int = 40
    max_size: int = 80
    show_coordinate: bool = True
    
tkk_config: RandomTkkConfig = RandomTkkConfig.parse_obj(nonebot.get_driver().config.dict())
TKK_PATH: Path = Path(tkk_config.tkk_path)