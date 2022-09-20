from nonebot import on_command
link= on_command('.link',aliases={'添加repo','添加项目'},priority=5)
linklist=on_command('.linklist',aliases={'查看repo','查看项目'})
linkdel=on_command('.linkdel',aliases={'删除repo','删除项目'})
linkset=on_command('linkset',aliases={'设置项目','设置repo'})