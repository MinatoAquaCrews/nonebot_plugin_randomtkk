from nonebot import on_command, on_regex, on_fullmatch
from nonebot.typing import T_State
from typing import List
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent, GroupMessageEvent
from nonebot.params import Depends, CommandArg, State, RegexMatched
from nonebot.rule import Rule
from .config import find_charac
from .handler import random_tkk_handler

__randomtkk_vsrsion__ = "v0.1.3rc1"
__randomtkk_notes__ = f'''
随机唐可可 {__randomtkk_vsrsion__}
[随机唐可可]+[简单/普通/困难/地狱/自定义数量] 开启寻找唐可可挑战
不指定难度则默认普通
答案格式：[答案是][行][空格][列]，例如：答案是114 514
[找不到唐可可] 发起者可提前结束游戏
将[唐可可]替换成其他角色可以寻找她们！'''.strip()

def inplaying_check(event: MessageEvent) -> bool:
    if isinstance(event, GroupMessageEvent):
        uuid = str(event.group_id)
    else:
        uuid = str(event.user_id)
        
    return random_tkk_handler.check_tkk_playing(uuid)

def starter_check(event: MessageEvent) -> bool:
    uid = str(event.user_id)
    if isinstance(event, GroupMessageEvent):
        gid = str(event.group_id)
    else:
        gid = None
        
    return random_tkk_handler.check_starter(gid, uid)

random_tkk = on_regex(pattern="^随机(.*) (帮助|简单|普通|困难|地狱|\d{1,2})?$", priority=12)
random_tkk_fullmatch = on_fullmatch(msg="随机唐可可", priority=12)
guess_tkk = on_command(cmd="答案是", rule=Rule(inplaying_check), priority=12, block=True)
surrender_tkk = on_regex(pattern="^找不到(.*)$", rule=Rule(starter_check), priority=12, block=True)

@random_tkk.handle()
async def _(matcher: Matcher, event: MessageEvent, matched: str = RegexMatched()):    
    uid = str(event.user_id)
    
    if isinstance(event, GroupMessageEvent):
        gid = str(event.group_id)
        if random_tkk_handler.check_tkk_playing(gid):
            await matcher.finish("游戏已经开始啦！", at_sender=True)
    else:
        if random_tkk_handler.check_tkk_playing(uid):
            await matcher.finish("游戏已经开始啦！")
        
    args: List[str] = matched.strip().split()
    
    user_input_charac = args[0][2:]
    charac = find_charac(user_input_charac)
    if not charac:
        await matcher.finish(f"角色名 {user_input_charac} 不存在，是不是记错名字了？")
        
    if len(args) == 1:
        await matcher.send("未指定难度，默认普通模式")
        level = "普通"
    elif len(args) == 2: 
        if args[1] == "帮助":
            await matcher.finish(__randomtkk_notes__)
        else:
            level = args[1]
    else:
        await matcher.finish("参数太多啦~")
    
    if isinstance(event, GroupMessageEvent):
        img_file, waiting = random_tkk_handler.one_go(matcher, gid, uid, level, user_input_charac)
    else:
        img_file, waiting = random_tkk_handler.one_go(matcher, uid, uid, level, user_input_charac)
    
    await matcher.send(MessageSegment.image(img_file))
    
    # 确保在此为send，超时回调内还需matcher.finish
    await matcher.send(f"将在 {waiting}s 后公布答案\n答案格式：[答案是][行][空格][列]\n例如：答案是114 514\n提前结束游戏请发起者输入[找不到{user_input_charac}]")
    
@random_tkk_fullmatch.handle()
async def _(matcher: Matcher, event: MessageEvent):
    uid = str(event.user_id)
    
    if isinstance(event, GroupMessageEvent):
        gid = str(event.group_id)
        if random_tkk_handler.check_tkk_playing(gid):
            await matcher.finish("游戏已经开始啦！", at_sender=True)
    else:
        if random_tkk_handler.check_tkk_playing(uid):
            await matcher.finish("游戏已经开始啦！")

    await matcher.send("未指定难度，默认普通模式")
    
    if isinstance(event, GroupMessageEvent):
        img_file, waiting = random_tkk_handler.one_go(matcher, gid, uid, "普通", "唐可可")
    else:
        img_file, waiting = random_tkk_handler.one_go(matcher, uid, uid, "普通", "唐可可")
    
    await matcher.send(MessageSegment.image(img_file))
    
    # 确保在此为send，超时回调内还需matcher.finish
    await matcher.send(f"将在 {waiting}s 后公布答案\n答案格式：[答案是][行][空格][列]\n例如：答案是114 514\n提前结束游戏请发起者输入[找不到唐可可]")

async def get_user_guess(args: Message = CommandArg(), state: T_State = State()):
    args = args.extract_plain_text().strip().split()

    if not args:
        await guess_tkk.finish("答案是啥捏？")
    elif len(args) == 1:    
        await guess_tkk.finish("答案格式错误~")
    elif len(args) == 2:
        args = [int(x) for x in args]   # 类型转换str -> int
        return {**state, "guess": args}
    else:
        await guess_tkk.finish("参数太多啦~")

@guess_tkk.handle()
async def _(event: MessageEvent, state: T_State = Depends(get_user_guess)): 
    pos = state["guess"]

    if isinstance(event, GroupMessageEvent):
        gid = str(event.group_id)
        if random_tkk_handler.check_answer(gid, pos):
            if not random_tkk_handler.bingo_close_game(gid):
                await guess_tkk.finish("结束游戏出错……")
            await guess_tkk.finish("答对啦，好厉害！", at_sender=True)
        else:
            await guess_tkk.finish("不对哦~", at_sender=True)
    else:
        uid = str(event.user_id)
        if random_tkk_handler.check_answer(uid, pos):
            if not random_tkk_handler.bingo_close_game(uid):
                await guess_tkk.finish("结束游戏出错……")
            await guess_tkk.finish("答对啦，好厉害！")
        else:
            await guess_tkk.finish("不对哦~")
        
@surrender_tkk.handle()
async def _(matcher: Matcher, event: MessageEvent, matched: str = RegexMatched()):
    arg = matched[3:]
    
    if isinstance(event, GroupMessageEvent):
        gid = str(event.group_id)
        if random_tkk_handler.check_surrender_charac(gid, arg):
            await random_tkk_handler.surrender(matcher, gid)
    else:
        uid = str(event.user_id)
        if random_tkk_handler.check_surrender_charac(uid, arg):
            await random_tkk_handler.surrender(matcher, uid)
    
    await matcher.finish(f"{arg} 与寻找的角色不匹配")