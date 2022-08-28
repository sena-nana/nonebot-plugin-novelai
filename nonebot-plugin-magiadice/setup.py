from setuptools import setup

setup(
    name='nonebot_plugin_magiadice',
    packages=['nonebot-plugin-magiadice'],
    version='0.1.2',
    description=(
        '一个基于nonebot的跑团LOG插件'
    ),
    author='sena-nana',
    author_email='851183156@qq.com',
    license='MIT License',
    platforms=["all"],
    url='https://github.com/sena-nana/MutsukiBot/tree/main/nonebot-plugin-magiadice',
    keywords=['nonebot','trpg','notion'],
    classifiers=[],
    install_requires=['notion','numpy','nonebot-adapter-onebot','nonebot2']
)