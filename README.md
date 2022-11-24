# 支持中文关键词的基于nonebot2的AI绘图插件
插件讨论反馈群：687904502
说明书：https://nb.novelai.dev

如果你是koishi框架的用户或者更熟悉Node.js，请出门左转[Novelai Bot](https://bot.novelai.dev/)

环境需求：
- Python>=3.8
- nonebot2>=b4
## 依赖
aiohttp,aiofiles

## 简要说明
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
    - [x] 支持文本生图
    - [x] 支持以图生图
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
    - [ ] 支持i18n
    - [ ] 支持多台后端负载均衡
    - [ ] 说明书
