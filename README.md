
# OpenAI.fm TTS 集成

在日常冲浪偶然发现这个网站，实际上它是用的网络早已经有人发现公开的方法，不过只是集成到自己网站中，但是我们可以利用它作为智能家居中继器。
这个自定义集成为Home Assistant添加了OpenAI.fm的文本转语音(TTS)能力，让您可以使用OpenAI.fm提供的高质量、自然的AI语音来朗读Home Assistant的通知和自动化消息

## 特点

- 支持多种高质量中文AI语音
- 可自定义提示词以控制语音风格
- 完全集成到Home Assistant的TTS服务中
- 实时显示TTS实体状态（准备中、播放中、错误）
- 通过配置UI轻松设置和管理

## 支持的语音

此集成支持OpenAI.fm提供的所有语音角色，包括：

- 知心姐姐
- 温柔女声
- 可爱萝莉
- 知性女声
- 标准女声 
- 温暖男声
- 磁性男声
- 标准男声
- 浑厚男声
...等等

## 安装

### 方法1：HACS (推荐)

1. 确保已安装[HACS]([url]https://hacs.xyz/[/url])
2. 在HACS中添加自定义仓库：
   - 点击HACS，选择"集成"
   - 点击右上角的菜单，选择"自定义仓库"
   - 输入 `knoop7/openai_fm`
   - 选择类别为"集成"
   - 点击"添加"
3. 在HACS商店中搜索并安装"OpenAI.fm TTS"
4. 重启Home Assistant

### 方法2：手动安装

1. 将此仓库中的`custom_components/openai_fm`文件夹复制到您的Home Assistant配置文件夹中的`custom_components`目录
2. 重启Home Assistant

## 配置

1. 在Home Assistant的设置中，进入"设备与服务"
2. 点击"添加集成"，搜索"OpenAI.fm"
3. 按照设置向导完成配置：
   - 选择您想要使用的AI语音
   - 设置自定义提示词（可选）

## 使用方法

安装并配置完成后，您可以在以下场景中使用此TTS服务：

### 在自动化中使用

```yaml
service: tts.openai_fm_say
data:
  entity_id: media_player.living_room_speaker
  message: "现在是晚上八点，该吃药了。"
  options:
    voice: "温柔女声"
```

### 在脚本中使用

```yaml
sequence:
  - service: tts.openai_fm_say
    target:
      entity_id: media_player.bedroom_speaker
    data:
      message: "闹钟已设置为明天早上七点。"
      options:
        voice: "标准男声"
        prompt: "请用平静的语调念出这段文字"
```

### 在Lovelace UI中使用

```yaml
type: button
name: 播放欢迎信息
tap_action:
  action: call-service
  service: tts.openai_fm_say
  service_data:
    entity_id: media_player.hallway_speaker
    message: "欢迎回家，希望您今天过得愉快。"
```

## 配置选项

| 选项 | 说明 | 默认值 |
|------|------|-------|
| `voice` | 要使用的语音 | `知性女声` |
| `prompt` | 自定义提示词，影响语音风格和语调 | `请用自然的语调念出这段文字` |

## 常见问题

### Q: 语音生成失败是什么原因？
A: 请检查您的网络连接，确保可以访问OpenAI.fm的API服务。该服务需要网络连接才能生成语音。

### Q: 我可以在离线环境中使用吗？
A: 不可以，此集成需要连接到OpenAI.fm的在线API才能生成语音。

### Q: 有使用限制吗？
A: 目前，OpenAI.fm提供免费的TTS服务，但可能有速率限制。请合理使用。

### Q: 如何更改语音？
A: 您可以在集成的配置页面修改默认语音，或在每次服务调用时通过`options`参数指定不同的语音。

## 免责声明

- 本集成由Knoop7开源开发，仅供学习和个人使用
- 不得用于商业用途，使用中产生的任何问题开发者不承担责任
- 使用本集成即表示您同意上述条款

## 隐私说明

此集成将您的文本内容发送到OpenAI.fm的API进行处理。请确保不要发送任何敏感或私密信息。

## 贡献

欢迎通过以下方式贡献：
- 提交错误报告和功能请求
- 提交Pull Request改进代码
- 分享您使用此集成的经验


*注意：OpenAI.fm是一个第三方服务，此集成不隶属于OpenAI.fm官方，也不受其支持或认可。*

[/md]

