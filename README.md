<div align="center">
  <a href="https://nb.novelai.dev"><img src="imgs/head.jpg" width="180" height="180" alt="NoneBot-plugin-novelai" style="border-radius:100%; overflow:hidden;"></a>
  <br>
</div>

<div align="center">

# Nonebot-plugin-novelai

_✨ 中文输入、对接 webui、以及你能想到的大部分功能 ✨_

[讨论群](https://jq.qq.com/?_wv=1027&k=pT3Mn4jG)|[说明书](https://nb.novelai.dev)|[整合包]()|[ENGLISH](./README_EN.md)

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/sena-nana/nonebot-plugin-novelai" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-novelai">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-novelai" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

> 请不要直接clone代码，主分支代码仅用作最新feature的体验，我并不保证其能够稳定运行，在重构期间甚至可能无法启动。如有下载必要，请从release中下载源代码

## 📖 功能介绍

- AI 绘画
  - 支持 CD 限速和绘画队列
  - 支持高级请求语法
  - 内置翻译 Api，自动翻译中文
  - 内置屏蔽词，可设置全局词条和排除词条
  - 返回消息支持简洁模式和详细模式
  - 模拟官方的点数管理模式，并能够按用户限制总额和每日使用量
  - 支持多后端负载均衡(Todo)
  - 支持自定义回复格式(Todo)
- 管理
  - 支持群黑白名单
  - 提供了管理指令用于运行时修改部分设置
  - Web 管理界面(Todo)
- 支持后端
  - novelai 官网
  - naifu
  - stable diffusion webui(本地，远程 or colab)
  - 另一个 novelai 插件(Todo)
  - 由第三方扩展的后端
- 扩展功能
  - 查询图片 TAG
  - 由第三方实现的扩展
- 自我管理
  - 版本检查和更新提醒，支持插件热更新和自动重启
  - 内置简易权限管理，被封退群，加群管理(Todo)

## 💿 安装
请前往说明书查看[安装](https://nb.novelai.dev/main/install.html)一节

## ⚙️ 配置

请前往说明书查看[全局配置](https://nb.novelai.dev/main/config.html)一节

## 🎉 使用

请前往说明书查看[使用](https://nb.novelai.dev/main/aidraw.html)一节

## 🌸 致谢

感谢[Novelai Bot](https://bot.novelai.dev/)提供的子域名，如果你更了解 Koishi 框架或是 Node.js，可以使用这个项目

感谢以下开发者对该项目做出的贡献：

<a href="https://github.com/sena-nana/nonebot-plugin-novelai/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=sena-nana/nonebot-plugin-novelai" />
</a>
