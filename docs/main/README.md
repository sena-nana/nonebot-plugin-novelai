---
title: AI绘图/novelai
order: 1
icon: creative
---

该插件允许你将 QQ 作为 AI 绘图的前端，支持的后端为 novalai 官方，naifu 和 webui

插件讨论反馈群：[687904502](https://jq.qq.com/?_wv=1027&k=3iIEAVBN)

## FEATURE

- 支持中文输入，内置 Bing 翻译(需申请 token)和有道翻译
- 支持对接多种绘画 AI 后端
- 支持限速和绘画队列

## 已实现功能

基于 NovelAI 的画图插件。已实现功能：

- 绘制图片
- 更改模型、采样器、图片尺寸
- 高级请求语法
- 自定义违禁词表
- 发送一段时间后自动撤回
- 连接到私服 · NAIFU，并支持多台后端负载均衡
- img2img
- 速率限制 (限制每个用户每天可以调用的次数和每次调用的间隔)
- 分群管理（无需打开后端即可更改某个群的设置而不影响其他群）
- 模拟官方的点数管理模式
- 支持本地化，用户自己的文件（以及萌萌语言 x）
- 支持其他插件制作扩展，以实现更加复杂的功能

## 须知

本插件使用 novelai 作为服务器时，需要使用 F12 自行抓取 token

本插件使用 naifu 作为后端时，需要服务器的 ip 和端口，由于 naifu 在传输过程中被多次修改，产生了许多不同的版本，各版本之间的部署方式可能不尽相同。

### 其他

如果你是 koishi 框架的用户或者更熟悉 Node.js，请出门左转[Novelai Bot](https://bot.novelai.dev/)

nonebot-plugin-novelai 和 Novelai Bot 各有擅长的部分和独特的功能，但是基本功能都能够完整的体验到。

相比之下，本插件的娱乐功能、扩展功能更加丰富，例如：

- 基于点数的管理模式
- 多台后端，多个模型负载均衡
- 自动对中文进行翻译
- 查 TAG 的功能
- 随机组合词条生成
- 查看其他人和自己的 XP
- 开放核心部分给其他插件供调用以扩展功能

等等

而 Novelai Bot 则依托于 Koishi 官方统一的插件标准，借助 Koishi 其他插件的功能，获得了更加精细的用户权限管理机制，模糊指令匹配，指令提示等。一些感觉没什么用的功能也没有在本插件中实现，例如切换至 furry 模型（如果真的有需求可以自己写插件调用）。

### 感谢

本说明很大一部分也参考了 Novelai Bot 的说明书，我实在不擅长过长的说明性内容的编写，所以没有 Novelai Bot 很可能没有这篇说明文档

感谢交流群的各位及时反馈各种奇奇怪怪的BUG以及提各种奇奇怪怪的需求，因为你们该插件才变得逐渐成熟完善

感谢Impact_XXX等用户帮忙测试内部版本、提供模型信息

感谢Nonebot2开发团队提供的机器人框架，（虽然有些地方怪怪的），但是习惯以后非常好用！