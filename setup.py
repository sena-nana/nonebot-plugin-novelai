# -*- coding: utf-8 -*-
from setuptools import setup

import codecs

with codecs.open("README.md", encoding="utf-8") as fp:
    long_description = fp.read()
with codecs.open("requirements.txt", encoding="utf-8") as fp:
    INSTALL_REQUIRES = fp.read().splitlines()

setup_kwargs = {
    "name": "nonebot-plugin-novelai",
    "version": "0.6.0",
    "description": "基于nonebot2的novelai绘图插件",
    "long_description": long_description,
    "license": "MIT",
    "author_email": "sena-nana <851183156@qq.com>",
    "url": "https://nb.novelai.dev",
    "packages": [
        "nonebot_plugin_novelai",
        "nonebot_plugin_novelai.backend",
        "nonebot_plugin_novelai.locales",
        "nonebot_plugin_novelai.utils",
        "nonebot_plugin_novelai.plugins",
        "nonebot_plugin_novelai.outofdate",
        "nonebot_plugin_novelai.web",
        "nonebot_plugin_novelai.version",
        "nonebot_plugin_novelai.mutsuki",
        "nonebot_plugin_novelai.extensions",
    ],
    "package_data": {"": ["*"]},
    "long_description_content_type": "text/markdown",
    "install_requires": INSTALL_REQUIRES,
    "python_requires": ">=3.8",
}


setup(**setup_kwargs)
