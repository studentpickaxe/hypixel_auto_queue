# Hypixel自动排队
## 使用方法
* 安装依赖：`pip install -r requirements.txt`
* 配置Minecraft日志路径，需要自动排队的游戏，和shout内容：`config.json`
  
  `minecraft_log`的`presets`可以是`vanilla`, `lunar`。若为其他内容，读取的Minecraft日志为`custom_location`中的路径。
* 运行：`py main.py`
