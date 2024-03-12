<div align="center">
  <a href="https://v2.nonebot.dev/store">
    <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="logo">
  </a>
  <br>
  <p>
    <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/NoneBotPlugin.svg" width="240" alt="logo">
  </p>
</div>

<div align="center">

# nonebot-plugin-a2s-query

*Nonebot2 查询游戏服务器详情*

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/NanakaNeko/nonebot-plugin-a2s-query.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-a2s-query">
	<img src="https://img.shields.io/pypi/v/nonebot-plugin-a2s-query.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

## 介绍

+ 基于value的a2s协议，可查询求生之路、半条命、军团要塞、Counter-Strike: Global Offensive、Counter-Strike 1.6、ARK: Survival Evolved、Rust等游戏  
+ 根据游戏服务器ip返回游戏内相关信息  
+ 已经实现文字转图，减少风控    

## 安装

<details open>
<summary>使用 nb-cli 安装（推荐）</summary>

```bash
nb plugin install nonebot-plugin-a2s-query
```
</details>

<details>
<summary>使用 pip 安装</summary>

```bash
pip intall nonebot-plugin-a2s-query
```

之后打开 nonebot2 项目根目录下的 pyproject.toml 文件, 在 [tool.nonebot] 部分追加写入
```bash
plugins = ["nonebot-plugin-a2s-query"]
```
</details>

## 使用

|          命令          | 权限 |                             介绍                             |                             示例                             |
| :--------------------- | :--- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| 查服 \| 查 \|  connect | 所有 |           查询服务器ip内详情，不加端口号默认27015            |   查服 测试 \| connect 192.168.0.1:27015 \| 查 192.168.0.1   |
|      加服 \| add       | 所有 | 在群里添加一个ip别称，方便查询，需要@机器人(别称和ip中间一定是英文的逗号，中文不会识别) | @bot 加服 测试,192.168.0.1:27015 \| @bot add test,192.168.0.1 |
|     删服 \| delete     | 所有 |                删除添加的ip别称， 需要@机器人                |              @bot 删服 测试 \| @bot delete test              |
| 订阅服 \| list \| 群服 | 所有 |                查询所有别称ip的服务器人数名称                |                     群服 \| list \| 群服                     |

## 图片示例

### 查服示例图片

![查服](./images/connect.png)

### 订阅服示例图片

![群服](./images/list.png)
