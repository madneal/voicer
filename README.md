春节在家一直闲着，今天有人给我发了一个小程序，即包你说。小程序是一个绕口令，很显然对于我这种 "n l" 不分的人说，这个绕口令也太难说了。因此我就想通过 python 脚本来实现。

![9tM3yF.png](https://s1.ax1x.com/2018/02/17/9tM3yF.png)

整个流程比较简单，主要是通过 adb 截取手机屏幕，获取口令的区域，然后通过百度的 OCR API 去识别口令获取文字，然后通过百度语音 API 去合成语音，通过 adb 模拟点击屏幕长按事件，最后通过电脑的 windows media player 播放 mp3 文件就可以了。

## adb

adb 可以通过开发者选项进行收集的控制。可以通过[安卓手机或模拟器操作步骤](https://github.com/wangshub/wechat_jump_game/wiki/Android-%E5%92%8C-iOS-%E6%93%8D%E4%BD%9C%E6%AD%A5%E9%AA%A4)里面的介绍安装 adb。在这个脚本里面，我们主要会用到两个命令:
```shell
// 截图
adb shell screencap -p
// 模拟长按屏幕 500 1000 为坐标位置，2000为长按持续时间
adb shell input swipe 500 1000 500 1000 2000
```

## 百度 API 

百度现在的确提供了很多 API，包括语音识别，语音合成以及 OCR 识别。可以在 http://yuyin.baidu.com/app 里面申请 API，通过创建应用并且申请 API 获取 APP_ID, APP_KEY, SECRET_KEY。通过使用百度的 python sdk 就可以轻易实现：

```python
# 离线合成语音
    client = AipSpeech(str(config_baidu['app_id']), config_baidu['api_key'], config_baidu['secret_key'])
    result = client.synthesis(text, 'zh', 1, {
        'vol': 5,
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('audio.mp3', 'wb') as f:
            f.write(result)
        f.close()
        
 # ocr 识别
    client = AipOcr(str(config_baidu['app_id']), config_baidu['api_key'], config_baidu['secret_key'])
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    image_data = img_byte_arr.getvalue()
    response = client.basicGeneral(image_data)
    words_result = response['words_result']
    texts = ''
    for x in words_result:
        texts += x['words']
    return texts
```

## 运行

本次脚本其实并没有特别的难度，主要就是其中几个流程搞清楚，主要是有几点可以注意一下。第一点就是截图区域的获得，比如口令的截图区域以及按钮的位置。另外，为了方便直接调用电脑的 windows media player 播放音频文件，因此注意修改程序的路径以及音频文件的绝对路径。

运行步骤：
* 手机连接电脑，确定打开开发者选项以及 USB 调试模式。
* 运行 `python app.py`

## 结语

花了一下午的时间写了这个脚本，其实脚本的难度并不大。python 语言作为一种脚本语言，的确在处理某些的确非常方便。怪不得，人生苦短，我用 python。通过这个脚本可以避免我拙劣的绕口令，可以通过阅读原文获取脚本的完整代码。

以上。

欢迎搜索微信号 mad_coder 或者扫描二维码关注公众号：

![9tMvlT.jpg](https://s1.ax1x.com/2018/02/17/9tMvlT.jpg)
