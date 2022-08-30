from setuptools import setup

setup(
    name='nonebot_plugin_ykt',
    packages=['nonebot-plugin-ykt'],
    version='0.1.3',
    description=(
        '一个基于nonebot的雨课堂自动签到插件'
    ),
    author='sena-nana',
    author_email='851183156@qq.com',
    license='MIT License',
    platforms=["all"],
    url='https://github.com/sena-nana/MutsukiBot/tree/main/nonebot-plugin-ykt',
    keywords=['nonebot','yuketang','playwright'],
    classifiers=[],
    install_requires=['playwright','nonebot-adapter-onebot','nonebot2']
)