<div align="center">
  <a href="https://nb.novelai.dev"><img src="imgs/head.jpg" width="180" height="180" alt="NoneBot-plugin-novelai" style="border-radius:100%; overflow:hidden;"></a>
  <br>
</div>

<div align="center">

# Nonebot-plugin-novelai

_✨ 中文输入、对接 webui、以及你能想到的大部分功能 ✨_

[讨论群](https://jq.qq.com/?_wv=1027&k=pT3Mn4jG)|[说明书](https://nb.novelai.dev)|[ENGLISH](./README_EN.md)

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/sena-nana/nonebot-plugin-novelai" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-novelai">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-novelai" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

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

<details>
<summary>使用 nb-cli 安装 (推荐)</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-novelai

</details>
<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的根目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-novelai

</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-novelai

</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-novelai

</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-novelai

</details>

打开 nonebot2 项目的 `pyproject.toml` 文档, 在其中 **plugins** 列表中，加入"nonebot-plugin-novelai"

</details>

## ⚙️ 配置

请前往说明书查看[全局配置](https://nb.novelai.dev/main/config.html)一节

## 🎉 使用

请前往说明书查看[使用](https://nb.novelai.dev/main/aidraw.html)一节