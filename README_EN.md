<div align="center">
  <a href="https://nb.novelai.dev"><img src="imgs/head.jpg" width="180" height="180" alt="NoneBot-plugin-novelai" style="border-radius:100%; overflow:hidden;"></a>
  <br>
</div>

<div align="center">

# Nonebot-plugin-novelai

_✨ Chinese input, sd-webui supported, and most other features you can imagine ✨_

[Discussing QQ group](https://jq.qq.com/?_wv=1027&k=pT3Mn4jG)|[Manual](https://nb.novelai.dev)|[中文](./README.md)

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/sena-nana/nonebot-plugin-novelai" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-novelai">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-novelai" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

## 📖 Feature introduction

- AI draw
  - CD speed limit and queues are supported.
  - Support for advanced commands
  - Built-in translation Api, automatic translation of Chinese(can be closed)
  - Built-in shielded words, you can set global tags and global ntags
  - The return message supports concise mode and detailed mode.
  - Simulates the official point management model with the ability to limit total and daily usage per user
  - Support for multiple back-end load balancing (Todo)
  - Support for custom reply Formats (Todo)
- Management
  - Support group chat black and white list
  - Provides commands for modifying some settings at run time
  - Web Management Interface (Todo)
- Back-ends
  - novelai
  - naifu
  - stable diffusion webui(Offline，Remote or Colab)
  - Another nonebot-plugin-novelai (Todo)
  - Backend extended by a third party
- Extension
  - Guess the tags of the picture
  - Extensions implemented by third parties
- Self-management
  - Version check and update reminder, support plug-in hot update and automatic restart
  - Built-in simple rights management, quit from group chat when being ban, and join group chat management (Todo)

## 💿 Install

<details>
<summary>Using nb-cli (Recommend)</summary>
Open the command line in the root directory of the nonebot2 project and enter the following instructions to install

    nb plugin install nonebot-plugin-novelai

</details>
<details>
<summary>Install using the package Manager</summary>
In the root directory of the nonebot2 project, open the command line and enter the appropriate installation command according to the package manager you are using

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

Open the `pyproject.toml` document of the nonebot2 project, and in the **plugins** list, add "nonebot-plugin-novelai"

</details>

## ⚙️ Config

Please go to the manual to see [Global configuration](https://nb.novelai.dev/main/config.html) section)

## 🎉 Use

Please go to the manual to see [Use] (https://nb.novelai.dev/main/aidraw.html) section
