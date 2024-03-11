import a2s
import ujson
from nonebot.plugin.on import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment, GroupMessageEvent
from nonebot.params import CommandArg
from nonebot.plugin import require, PluginMetadata
require("nonebot_plugin_txt2img")
from nonebot_plugin_txt2img import Txt2Img
require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store
from pathlib import Path, PurePath

__plugin_meta__ = PluginMetadata(
    name="a2s查询",
    description="查询value服务器详情",
    usage="查服;加服;删服;订阅服",
    type="application",
    homepage="https://github.com/NanakaNeko/nonebot-plugin-a2s-query",
    supported_adapters={"~onebot.v11"},
    extra={},
)

data_file = store.get_data_file("nonebot-plugin-a2s-query", "a2s.json")
data_dir = store.get_data_dir("nonebot-plugin-a2s-query")
if not Path.exists(data_file):
    with open(PurePath.joinpath(data_dir, "a2s.json"), "w", encoding="utf-8") as f:
      f.write('{}')



ca2s = on_command("查服", aliases={'connect','查'}, priority=5, block=True)
wa2s = on_command("加服", aliases={'add'}, priority=5, block=True)
da2s = on_command("删服", aliases={'delete'}, priority=5, block=True)
sa2s = on_command("订阅服", aliases={'list','群服'}, priority=5, block=True)

@ca2s.handle()
async def search(event: GroupMessageEvent, msg: Message = CommandArg()):
    host = msg.extract_plain_text().strip()
    group = str(event.group_id)
    
    if("." in host):
        if(":" in host):
            ip = host.split(':')[0]
            port = int(host.split(':')[1])
        else:
            ip = host
            port = 27015
    else:
        content = readInfo(data_file)
        try:
            host = content[group][host]
            if(":" in host):
                ip = host.split(':')[0]
                port = int(host.split(':')[1])
            else:
                ip = host
                port = 27015
        except KeyError:
            await ca2s.finish("未绑定服务器！")

    address = (ip, port)
    hostinfo = f"服IP:{ip}:{port}"
    try:
        server_name = a2s.info(address).server_name
        map_name = a2s.info(address).map_name
        ogame = a2s.info(address).folder
        if ogame.find("left4dead2") == -1:
            gamename = f"游戏:{ogame}"
        else:
            gamename = "游戏:求生之路2"
        game = a2s.info(address).game
        ping = int(a2s.info(address).ping*1000)
        player_count = a2s.info(address).player_count
        max_players = a2s.info(address).max_players
        title = f"服名:{server_name}\n地图:{map_name}\n描述:{game}\n人数:[{player_count}/{max_players}] | 延迟:{ping}ms\n"
        if(player_count == 0):
            playerinfo = "\n服务器里面是空的哦~\n"
        else:
            listplayers = a2s.players(address)
            playerinfo = "----------------------------\n|  分数  |    时间    |      玩家      |\n----------------------------\n"
            for player in listplayers:
                playername = player.name
                playerscore = player.score
                playertime = int(player.duration)
                m, s = divmod(playertime, 60)
                h, m = divmod(m, 60)
                if(h == 0):
                    if(m == 0):
                        hms = "%ds" % s
                    else:
                        hms = "%dm%ds" % (m, s)
                else:
                    hms = "%dh%dm%ds" % (h, m, s)
                playerinfo += f"◆ {playerscore} | {hms} | {playername}\n"
        result = f"{title}{playerinfo}\n{hostinfo}"
        txt2img = Txt2Img()
        # 设置字体大小
        txt2img.set_font_size(28)
        # 绘制 ByteIO 图片并发送
        msgs = MessageSegment.image(txt2img.draw(gamename, result))
    except:
        msgs = Message("查询失败，请重新尝试")
    await ca2s.finish(msgs)

@wa2s.handle()
async def add(event: GroupMessageEvent, msg: Message = CommandArg()):
    args = msg.extract_plain_text().strip()
    if(',' in args):
        cmd_name = args.split(',')[0].strip()
        cmd_host = args.split(',')[1].strip()
        group = str(event.group_id)
        content = readInfo(data_file)
        try:
            if content[group]:
              pass
        except KeyError:
            content[group] = {}
        try:
            if content[group][cmd_name]:
                await wa2s.finish(Message(f"{cmd_name}已经添加过了！"), at_sender=True)
        except KeyError:
            content[group][cmd_name] = cmd_host
            readInfo(data_file, content)
            await wa2s.finish(Message(f"{cmd_name}添加成功！"), at_sender=True)
    else:
        await wa2s.finish(Message("输入有误！"), at_sender=True)
  
@da2s.handle()
async def delete(event: GroupMessageEvent, msg: Message = CommandArg()):
    cmd_name = msg.extract_plain_text().strip()
    group = str(event.group_id)
    content = readInfo(data_file)
    try:
        if content[group][cmd_name]:
            content[group].pop(cmd_name)
            readInfo(data_file, content)
            await da2s.finish(Message(f"{cmd_name}成功删除！"), at_sender=True)
    except KeyError:
        await da2s.finish(Message(f"{cmd_name}未添加！"), at_sender=True)

@sa2s.handle()
async def search_all(event: GroupMessageEvent):
    group = str(event.group_id)
    content = readInfo(data_file)
    try:
        if content[group]:
          pass
    except KeyError:
        await sa2s.finish(Message("暂无添加订阅！"), at_sender=True)
    try:
        infos = ""
        for name in content[group]:
            try:
                if(":" in content[group][name]):
                    ip = content[group][name].split(':')[0]
                    port = int(content[group][name].split(':')[1])
                else:
                    ip = content[group][name]
                    port = 27015
                ads = (ip, port)
                sname = a2s.info(ads).server_name
                num = a2s.info(ads).player_count
                maxnum = a2s.info(ads).max_players
                infos += f"★{name}☆{sname}({num}/{maxnum})\n"
            except:
                infos += f"★{name}☆查询失败\n"
                continue

        txt2img = Txt2Img()
        # 设置字体大小
        txt2img.set_font_size(28)
        # 绘制 ByteIO 图片并发送
        msgs = MessageSegment.image(txt2img.draw("订阅服务器", infos))
        await sa2s.finish(msgs)
    except KeyError:
        await sa2s.finish(Message("暂无添加订阅！"), at_sender=True)
  
def readInfo(file, info=None):
    """
    读取文件信息
    """
    context = file.read_text()
    if info != None:
        file.write_text(ujson.dumps(info, indent=4, ensure_ascii=False))
        return {"data": ujson.loads(context.strip())}
    else:
        return ujson.loads(context.strip())
