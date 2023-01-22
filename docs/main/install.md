---
title: 安装
icon: markdown
order: 2
tag:
  - Markdown
---


<details>
<summary>使用 nb-cli 安装 (推荐)</summary>

1. 在 nonebot2 项目的根目录下打开终端
2. 如果你是 Windows 用户，输入`./.venv/Scripts/activate`并回车，如果你是 Linux 用户，输入`source ./.venv/bin/activate`并回车。你应该能够看到终端在新的一行激活了虚拟环境。如果你使用旧版 nb-cli 创建的项目不存在.venv 文件夹，则跳过此步骤

3. 最后输入以下指令即可安装

```
nb plugin install nonebot-plugin-novelai
```

</details>
<details>
<summary>使用包管理器安装</summary>

1. 在 nonebot2 项目的根目录下, 打开终端
2. 如果你是 Windows 用户，输入`./.venv/Scripts/activate`并回车，如果你是 Linux 用户，输入`source ./.venv/bin/activate`并回车。你应该能够看到终端在新的一行激活了虚拟环境。如果你使用旧版 nb-cli 创建的项目不存在.venv 文件夹，则跳过此步骤
3. 根据你使用的包管理器, 输入相应的安装命令

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

4. 打开 nonebot2 项目的 `pyproject.toml` 文档, 在其中名为 **plugins** 的列表中，加入"nonebot-plugin-novelai"

</details>
<details>
<summary>下载源码安装 (不推荐)</summary>

> 除非你对自己解决问题的能力有信心，并且有着修改插件的需求，否则你不应该选择这种方法。这种方法无法通过以上两种方法更新版本，并会与插件内置的更新功能冲突

1. (nb-cli 版本 1.0 以上) 确保你在创建项目时选择的是开发者版项目结构，否则插件目录中不存在能够放置插件的文件夹。
2. 在 nonebot2 项目的根目录下打开命令行
3. 如果你是 Windows 用户，输入`./.venv/Scripts/activate`并回车，如果你是 Linux 用户，输入`source ./.venv/bin/activate`并回车。你应该能够看到终端在新的一行激活了虚拟环境。如果你使用旧版 nb-cli 创建的项目不存在.venv 文件夹，则跳过此步骤
4. 在 Github 中下载源代码
   1. [稳定版本](https://github.com/sena-nana/nonebot-plugin-novelai/releases/download/v0.6.0/nonebot_plugin_novelai.zip)
   2. [测试版本](https://github.com/sena-nana/nonebot-plugin-novelai/archive/refs/heads/main.zip)
5. 将上一步下载的 zip 文件打开，将**requirements.txt**复制至 bot 项目根目录备用，将**nonebot_plugin_novelai**文件夹解压至 bot 目录的 src/plugins 文件夹中
6. 在终端中运行下面的指令，如果你使用pip以外的包管理器，请使用对应的指令

```
pip install -r requirements.txt
```

7. 现在你可以删除**requirements.txt**文件了

</details>