# 支持中文关键词的基于nonebot2的AI绘图插件
插件讨论反馈群：687904502
说明书：https://sena-nana.github.io/MutsukiDocs/

环境需求：
- Python>=3.8
- nonebot2>=b4
## 依赖
aiohttp,aiofiles
## 配置文件
如果你使用官方服务器，需要将以下信息写入env文件(目前必须填)

1. NOVELAI_TOKEN="str"   你的Novelai token，需要f12抓取

可选信息

1. NOVELAI_TAG="str"   所有生成都会事先加上这些tag，用来塞私货或者精简指令
2. NOVELAI_CD=int   单个用户的cd，默认为60s
3. NOVELAI_LIMIT=bool   是否启用并行限制，启用的话，bot会将请求加入队列，在服务器返回之前的结果后再申请。可以防止请求过快，在不知道官方会不会封号的情况下有心理安慰作用。默认开启
5. NOVELAI_SITE="str"  自定义后端时设置
6. NOVELAI_SAVE=int  是否自动保存到本地，默认开启（1）
7. NOVELAI_MODE="str"   设置插件运行模式，默认"novelai"，详细查看说明书（还没写）
8. NOVELAI_PAID=int   是否启用已付费模式,默认为0（禁用），1为点数模式，2为严格点数模式，3为无限制模式
9. NOVELAI_DAYLIMIT=int 是否启用每日次数限制，默认为0（禁用），值为次数
9. NOVELAI_BAN=list[int] 设置在哪些群禁用，默认为空，运行时可通过指令修改
10. NOVELAI_H=bool 是否启用r18模式，默认关闭（开启后被风控或者封号不要发issue）
10. NOVELAI_ONCEMAX=int 单次允许生成的最大数量
10. NOVELAI_REVOKE=int 是否自动撤回

## 说明
该插件允许在nonebot2前端软件中使用ai绘图，支持的后端为novalai官方，naifu和webui

novelai模式需要token才能运行，所以你需要首先购买novelai的25刀套餐（25刀套餐支持无限生成）。其他套餐也支持，但是会扣费。
## 指令示例

.aidraw loli,cute --ntags big breast --seed 114514
- 指令使用shell解析输入的参数
- square为指定画幅，支持简写为s，其他画幅为portrait和landscape，同样支持简写，默认为portrait
- seed若省略则为自动生成
- 词条使用英文，使用逗号（中英都行，代码里有转换）分割，中文会自动机翻为英文，不支持其他语种
- 如果你不想用.aidraw，可以用 **绘画** 、 **咏唱** 或 **召唤** 代替。
- 在消息中添加图片或者回复带有图片的消息自动切换为以图生图模式

.aidraw on/off
- 启动/关闭本群的aidraw

.anlas check
- 查看自己拥有的点数

.anlas
- 查看帮助

.anlas [数字] @[某人]
- 将自己的点数分给别人(superuser点数无限)

.tagget [图片]
- 获取图片的TAG
- 如果你不想用.tagget，可以用 **鉴赏** 或 **查书** 代替。

## FEATURE
- NAIFU
    - [x] 支持文本生图
    - [x] 支持以图生图
- WEBUI
    - [ ] 支持文本生图
    - [ ] 支持以图生图
- NOVELAI
    - [x] 支持文本生图
    - [x] 支持以图生图
- OTHERS
    - 群聊管理
        - [x] 支持分群设置
    - 速度限制
        - [x] 支持内置CD和并行限制
        - [x] 付费点数制
        - [x] 严格点数制
        - [x] 每日上限制
    - 娱乐功能
        - [x] 支持查询图片词条
        - [ ] 随机少女
        - [ ] 内置咒语集
        - [ ] 支持数据统计
    - 命令处理（需要重构）
        - [x] 支持文字生图画幅指定，种子指定
        - [x] 支持输入排除词条
        - [x] 支持批量生成
    - 命令优化
        - [x] 内置优化词条模板并自动使用
        - [x] 支持管理员塞私货
        - [x] 支持机翻词条为英文
    - [x] 生成图片自动保存至data/novelai文件夹
    - [x] 支持开关禁止nsfw
    - [x] 更新提醒
    - [ ] 支持多台后端负载均衡
    - [ ] 说明书