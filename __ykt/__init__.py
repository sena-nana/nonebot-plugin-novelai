from nonebot import require
from playwright.async_api import async_playwright
import nonebot
from nonebot import on_command
from nonebot import get_driver
from nonebot.adapters.onebot.v11 import Bot
username = get_driver().config.username
password = get_driver().config.password
url = 'https://changjiang.yuketang.cn/v2/web/index'
scheduler = require("nonebot_plugin_apscheduler").scheduler
superuser = get_driver().config.master
async def send_success(lesson,meeting,video):
    for bot in nonebot.get_bots().values():
        if meeting:
            message = lesson[0]+" 有会议喵！"+meeting[0]
        elif video:
            message = lesson[0]+" 签到完成了喵！当前课程有视频直播喵！"
        else:
            message = lesson[0]+" 签到完成了喵！"
        await bot.call_api('send_msg', **{
            'message': message,
            'user_id': superuser
        })



async def yktcheckin():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(storage_state="cookie")
        page = await context.new_page()
        await page.goto(url)
        if page.url != url:
            await page.locator("img[alt=\"账号密码登录\"]").click()
            await page.locator("[placeholder=\"输入手机号\"]").first.fill(username)
            await page.locator("[placeholder=\"输入密码\"]").first.fill(password)
            async with page.expect_navigation():
                await page.locator(".submit-btn").first.click()
            await context.storage_state(path="cookie")
        if await page.is_visible('.onlesson'):
            await page.click('.onlesson')
            items = await page.locator('.lessonTitle').all_text_contents()
            async with page.expect_popup() as popup_info:
                await page.locator(".lessonTitle").click()
            page1 = await popup_info.value
            meeting = None
            video= False
            await page1.wait_for_timeout(5000)
            if await page1.is_visible('.video__anchors'):
                video = True
            if await page1.is_visible(".txmeet__join"):
                await page1.locator(".txmeet__join").click()
                meeting = await page1.locator("#tm-meeting-info").all_text_contents()
            await send_success(items, meeting,video)
            await browser.close()
            return True
        else:
            await browser.close()
            return False
@scheduler.scheduled_job("cron", hour='8,14',id="ykt1", day_of_week='0-4')
async def tkt1():
    await yktcheckin()


@scheduler.scheduled_job("cron", hour='10,16', minute = 8,id="ykt2", day_of_week='0-4')
async def tkt2():
    await yktcheckin()

yktcheckin_command = on_command("ykt",priority=5)

@yktcheckin_command.handle()
async def ykt_receive():
    success = await yktcheckin()
    if not success:
        await yktcheckin_command.finish(f'现在还没有上课喵~')

