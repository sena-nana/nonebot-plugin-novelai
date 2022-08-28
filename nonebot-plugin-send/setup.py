from setuptools import setup

setup(
    name='nonebot_plugin_send',
    packages=['nonebot-plugin-send'],
    version='0.1.2',
    description=(
        '一个基于nonebot的反馈通知插件'
    ),
    author='sena-nana',
    author_email='851183156@qq.com',
    license='MIT License',
    platforms=["all"],
    url='https://github.com/sena-nana/MutsukiBot/tree/main/nonebot-plugin-send',
    keywords=['nonebot'],
    classifiers=[],
    install_requires=['nonebot-adapter-onebot','nonebot2']
)