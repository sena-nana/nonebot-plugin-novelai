---
title: Install
icon: markdown
order: 2
tag:
  - Markdown
---

<details>
<summary>Install using nb-cli (recommended)</summary>

1. Open the terminal in the root directory of the nonebot2 project
2. If you are a Windows user, enter `./.venv/Scripts/activate` and enter. If you are a Linux user, enter `source ./.venv/bin/activate` and enter.You should be able to see the terminal activate the virtual environment on the new line.
If the project you created with older nb-cli does not exist in the .venv folder, skip this step

3. Finally, enter the following instructions to install

```
nb plugin install nonebot-plugin-novelai
```

</details>
<details>
<summary>Install using the package Manager</summary>

1. Open the terminal in the root directory of the nonebot2 project
2. If you are a Windows user, enter `./.venv/Scripts/activate` and enter. If you are a Linux user, enter `source ./.venv/bin/activate` and enter.You should be able to see the terminal activate the virtual environment on the new line.
If the project you created with older nb-cli does not exist in the .venv folder, skip this step
3. According to the package manager you use, enter the appropriate installation command

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

4. Open the `pyproject.toml` document of the nonebot2 project, and in the list named **plugins**, add "nonebot-plugin-novelai"

</details>
<details>
<summary>install using source code (not recommended)</summary>

> Unless you have confidence in your problem-solving ability and have the need to modify plugin, you should not choose this approach.This method cannot update the version through the above two methods, and will conflict with the update feature of the plugin

1. (nb-cli version 1.0 +) make sure you choose the developer version project structure when creating the project, otherwise there is no folder in the plug-in directory where you can place plug-ins.
2. Open the terminal in the root directory of the nonebot2 project
3. If you are a Windows user, enter `./.venv/Scripts/activate` and enter. If you are a Linux user, enter `source ./.venv/bin/activate` and enter.You should be able to see the terminal activate the virtual environment on the new line.
If the project you created with older nb-cli does not exist in the .venv folder, skip this step
4. Download the source code in Github
   1. [Stable Version](https://github.com/sena-nana/nonebot-plugin-novelai/releases/download/v0.6.0/nonebot_plugin_novelai.zip)
   2. [Nightly Version](https://github.com/sena-nana/nonebot-plugin-novelai/archive/refs/heads/main.zip)
5. Open the zip file downloaded in the previous step, copy the **requirements.txt** to the root directory of the bot project, and extract the **nonebot_plugin_novelai** folder to the src/plugins folder in the bot directory.
6. Run the following instructions in the terminal. If you are using a package manager other than pip, please use the corresponding instructions

```
pip install -r requirements.txt
```

7. Now you can delete the **requirements.txt** file.
</details>
