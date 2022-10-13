# 基于nonebot2的Novelai绘图插件
环境需求：
- Python>=3.10，低版本python请自行clone然后修改match部分代码
- nonebot2>=rc1，如果不符合版本安装时会强制升上去然后你的其他一大堆插件就会爆炸
## 依赖
aiohttp,aiofiles
## 配置文件
如果你使用官方服务器，需要将以下信息写入env文件(目前必须填)

1. NOVELAI_TOKEN="str"   你的Novelai token，需要f12抓取

可选信息

1. NOVELAI_TAG="str"   所有生成都会事先加上这些tag，用来塞私货或者精简指令
2. NOVELAI_CD=int   单个用户的cd，默认为60s
3. NOVELAI_LIMIT=bool   是否启用并行限制，启用的话，bot会将请求加入队列，在服务器返回之前的结果后再申请。可以防止请求过快，在不知道官方会不会封号的情况下有心理安慰作用。默认开启
4. NOVELAI_API_DOMAIN="str"  白嫖服务器时修改，不设置默认官方服务器(未完成)
5. NOVELAI_SITE_DOMAIN="str"  白嫖服务器时修改，不设置默认官方服务器(未完成)
6. NOVELAI_SAVE_PIC=bool  是否自动保存到本地，默认开启
7. NOVELAI_MODE="str"   设置插件运行模式，默认"novelai"，详细查看说明书（还没写）
8. NOVELAI_PAID=bool   是否启用已付费模式,默认关闭（当前没有用）
9. NOVELAI_PAN=list[int] 设置在哪些群禁用，默认为空，运行时可通过指令修改
10. NOVELAI_H=bool 是否启用r18模式，默认关闭（开启后被风控或者封号不要发issue）

## 说明
该插件爬取novelai以允许在nonebot2前端软件中使用ai绘图

插件需要novelai的token才能运行，所以你需要首先购买novelai的25刀套餐（25刀套餐支持无限生成）。其他套餐也支持，但是会扣费。
## 指令示例

.aidraw -seed-square-cute,loli,kawaii,
- 指令使用-来分割各个部分，如果你只输入词条可以不用加-
- square为指定画幅，支持简写为s和S，其他画幅为portrait和landscape，同样支持简写，默认为portrait
- seed若省略则为自动生成
- 词条使用英文，使用逗号（中英都行，代码里有转换）分割，中文会自动机翻为英文，不支持其他语种

.aidraw on/off
- 启动/关闭本群的aidraw

## FEATURE
- [x] 内置优化词条模板并自动使用
- [x] 生成图片自动保存至data/novelai文件夹
- [x] 支持文字生图画幅指定，种子指定
- [x] 支持管理员塞私货
- [x] 支持内置CD和并行限制
- [x] 支持开关禁止nsfw
- [ ] 支持输入排除词条
- [ ] 支持以图生图
- [ ] 支持衍生
- [ ] 支持细化
- [x] 支持开启关闭功能
- [x] 支持机翻词条为英文
- [ ] 支持自搭服务器
- [ ] 支持白嫖别人的自搭服务器
- [ ] 支持数据统计
- [ ] 支持私聊