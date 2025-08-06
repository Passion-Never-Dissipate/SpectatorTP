# SpectatorTP
> 你还在为观察者模式下无法tp观察者玩家烦恼吗？还在为观察者模式下无法穿过地狱门而烦恼吗？来看看这款插件吧

一个专为观察者模式设计的多模式传送插件，在开始使用前建议你详细阅读下文档

您在使用过程中遇到任何问题或想提出建议，欢迎加入我们的交流群号: 417086159

> [!WARNING]
>
> 使用此插件前，请确保您的服务端已经安装能够在生存模式与观察者模式间来回切换的插件，如[Gamemode](https://github.com/AnzhiZhang/MCDReforgedPlugins/tree/master/src/gamemode)
> 
> 本插件只能在观察者模式或创造模式下工作。

## 前置插件
* [MinecraftDataAPI](https://github.com/Fallen-Breath/MinecraftDataAPI)

## 指令使用说明

`!!st help` 显示帮助信息

`!!st`/`!d` 根据当前坐标在地狱和主世界间快速切换，自身必须是非生存模式且处于地狱与主世界间的任一维度

`!!st id <玩家>` 传送到某个玩家，自身必须是非生存模式

`!!st id <玩家1> <玩家2>` 将玩家1传送到玩家2，玩家1必须是非生存模式

`!!st <x> <y> <z>` 传送到自身所在维度的指定坐标,自身必须是非生存模式

`!!st <x> <y> <z> in <维度:0主世界,-1地狱,1末地>` 传送到某个维度的指定坐标,自身必须是非生存模式

## 配置文件说明

* ### dim_convert
  
  默认值：

>``` 
>   {
>        "0": "minecraft:overworld",
>        "-1": "minecraft:the_nether",
>        "1": "minecraft:the_end"
>    }
>```

  一个字典，代表维度数字id与维度名称之间的映射，原版环境下你不需要修改它

* ### dim_translation
  
  默认值：

>``` 
>   {
>        "minecraft:overworld": "主世界",
>        "minecraft:the_nether": "下界",
>        "minecraft:the_end": "末地"
>    }
>```

  一个字典，代表维度名称与维度翻译文本之间的映射，原版环境下你不需要修改它

* ### prefix

  默认值: !!st

  插件指令的前缀，在指令未与其他插件起冲突的情况下，你最好不要更改它

* ### short_prefix

  默认值: !d

  短命令的前缀，如果你不知道它是什么，不要更改它

* ### short_prefix_enable  

  默认值: true

  短命令的开关
