# 魔法崩坏骰娘+TRPGLOG插件
## 依赖
如直接下载到插件文件夹，以下依赖需自行pip安装，通过nb或pip安装不需要

1. numpy
2. notion
## 配置文件

1. superuser：（nb内置参数）你的qq号
2. token：notion的cookie中的token_v2，需要自行用f12查看
3. database：用来作为LOG总目录的页面id（即地址后面的乱码部分）
4. sendtomaster：布尔值，有人使用log时是否通知superuser
   
## 说明

[魔法崩坏规则](https://sena-nana.github.io)是一个魔法少女世界观的跑团规则。

该骰娘最初专门为魔法崩坏开发，包含了魔法崩坏一版规则书的指令以及coc规则的rd，ra指令。目前正在适配coc，dnd等规则的其他指令。

LOG部分使用了notion作为服务器，支持实时在线更新和围观，支持实时颜色渲染、对话筛选分类、图片线索。

[所有log的目录](https://senanana.notion.site/TRPGLOG-98acc03f3dae47a398516dc4bba11aad)，可以点击查看其他人的跑团log及效果预览。

骰娘部分与LOG部分绑定，LOG会将骰娘的返回值特殊处理，并加入LOG中。若想使用其他骰娘，请让骰娘按照玩家的方式加入游戏，后续会对其他骰娘加入进行适配。

## 指令
### 骰娘部分
1. .magia：进行一次魔法崩坏一版规则的快速车卡
2. .ra
3. .rd
4. .msc：魔法崩坏一版规则的sc检定，与coc不通用
5. .mhelp：说明书
### LOG部分
1. .log on <gameid> 开始记录(不传id）/使用id继续记录
2. .log in <charaname> 加入游戏(不传名字则使用昵称)
3. .log off 结束记录（记录十小时后自动停止）
4. .log name [title] 设置记录的标题(默认为日期)
5. .log intro [data] 添加介绍（添加在LOG开始的模组介绍中）
6. .log change [x] [data] 修改第x条模组介绍（不传data为删除）"""
### LOG记录流程
1. logon初始化LOG页面，输入该指令的人会自动登陆为KP
2. login玩家加入（必须,否则LOG无法判断玩家是谁从而自动筛选）
3. logname，logintro（可选非必须）修改log的标题和介绍
4. logoff结束记录