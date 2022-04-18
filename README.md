<div align="center">
    <img width="200" src="tkk_logo.png" alt="logo"></br>

# Random Tan Kuku

<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD036 -->
_🎶 随机唐可可 🎶_
<!-- prettier-ignore-end -->

</div>
<p align="center">
  
  <a href="https://github.com/MinatoAquaCrews/nonebot_plugin_randomtkk/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/MinatoAquaCrews/nonebot_plugin_randomtkk?color=blue">
  </a>

  <a href="https://github.com/nonebot/nonebot2">
    <img src="https://img.shields.io/badge/nonebot2-2.0.0beta.2-green">
  </a>

  <a href="https://github.com/MinatoAquaCrews/nonebot_plugin_randomtkk/releases/tag/v0.1.0">
    <img src="https://img.shields.io/github/v/release/MinatoAquaCrews/nonebot_plugin_randomtkk">
  </a>
  
</p>

</p>

## 版本

v0.1.1

⚠ 适配nonebot2-2.0.0beta.2

[更新日志](https://github.com/MinatoAquaCrews/nonebot_plugin_randomtkk/releases/tag/v0.1.1)

## 安装

1. 通过`pip`或`nb`安装；

2. 随机唐可可图片等资源位于`./resource`下，可在`env`下设置`TKK_PATH`更改；

    ```python
    TKK_PATH="your_path_to_resource"
    ```

3. 可更改默认配置：

    ```python
    TKK_PATH="./data/resource"  # 可自定义资源路径，例如
    EASY_SIZE=10                # 简单
    NORMAL_SIZE=20              # 普通
    HARD_SIZE=40                # 困难
    EXTREME_SIZE=60             # 地狱
    MAX_SIZE=80                 # 自定义的最大尺寸，建议不要太大
    SHOW_COORDINATE=true        # 是否显示坐标文字
    ```

    注意图片最小尺寸为10，最大尺寸可通过`MAX_SIZE`修改（默认80），但生成时间会变长；`SHOW_COORDINATE`开启会在生成的图片方阵中显示坐标。
    
    ⚠ 资源路径错误或缺少资源会在启动时报错，此时无法开始游戏。

4. 呜↗太⬆好⬇听↙了↖吧↗你唱歌真的好好听啊，简直就是天籁！我刚才，听到你唱歌了。我们以后一起唱好不好？一起唱！一起做学园偶像！

## 功能

寻找唐可可！

**新增** 支持私聊。

## 命令

1. 开始游戏：[随机唐可可/鲤鱼/鲤鱼王/Liyuu/liyuu]+[简单/普通/困难/地狱/自定义数量]，不指定难度默认普通，开始游戏后会限时挑战；

2. 输入答案：[答案是][行][空格][列]，行列为具体数字，例如：答案是114 514；

3. 答案正确则结束此次游戏；不正确则直至倒计时结束，Bot公布答案并结束游戏；

4. 提前结束游戏：[找不到唐可可/唐可可人呢/呼叫鲤鱼姐]，仅**游戏发起者**可提前结束游戏；

5. 各群聊互不影响，每个群聊仅能同时开启一局游戏。

## 本插件改自

[Hoshino-randomtkk](https://github.com/kosakarin/hoshino_big_cockroach)

很早就想改这个插件适配到nb2上了。
