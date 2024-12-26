import random
from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
# 機器人回覆套件區：
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage, # 文字訊息套件
    ImageMessage, # 圖片訊息套件
    LocationMessage, # 地標訊息套件
    AudioMessage, # 音訊訊息套件
    VideoMessage, # 影片訊息套件
    StickerMessage, # 貼圖訊息套件
    Emoji # Emoji套件
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
import os

app = Flask(__name__)

# 環境變數：在 Vercel 伺服器裡面設定，網址：https://vercel.com/tiffanylinnnns-projects/ncuuulinebot/settings/environment-variables
configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
linehandlers = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# App Webhook：在 Line Developer 裡面抓取程式碼的地方，網址：https://developers.line.biz/console/channel/2006724665/messaging-api
# 基本上這邊不用修改。
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        linehandlers.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 處理訊息事件
@linehandlers.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # text：你抓到的訊息
    text = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if text == '嗨1~~!':
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        TextMessage(text="嗨，我是ncuuulinebot機器人~~\n幫大家紀錄了碩班這兩年的快樂時光ㄏㄏ")
                    ]
                )
            )

        elif text == '我要抽表情符號':
            # Emojis 陣列：儲存你的表情符號資料，如果觸發才會回覆以下表情符號
            emojis = [
                # index：索引值、product_id：表情符號庫、emoji_id：第幾張表情符號
                # 網址：https://developers.line.biz/en/docs/messaging-api/emoji-list/#line-emoji-definitions
                Emoji(index=0, product_id="5ac1bfd5040ab15980c9b435", emoji_id="001"),
                Emoji(index=12, product_id="5ac1bfd5040ab15980c9b435", emoji_id="002")
            ]
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        # $ 的位置會放表情符號，依照 index 順序放，以字數計算
                        TextMessage(text='$ Line 表情符號 $', emojis=emojis)
                    ]
                )
            )

        elif text == '我要抽貼圖':
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        # package_id：貼圖庫、sticker_id：第幾張貼圖
                        # 網址：https://developers.line.biz/en/docs/messaging-api/sticker-list/#sticker-definitions
                        StickerMessage(package_id="446", sticker_id="1988")
                    ]
                )
            )

        elif text == '抽抽':
            # 隨機亂數：從 1 ~ 10 裡面隨機挑選一個數字
            image_index = str(random.randint(1,73))
            # 圖片位址：讓 Vercel 伺服器知道你的圖片位址在哪裡（範例：static/images/image1.jpg）
            url = request.url_root + 'static/images/image' + image_index + '.jpg'
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(original_content_url=url, preview_image_url=url)
                    ]
                )
            )
        
        elif text == '我要抽聲音':
            # 隨機亂數：從 1 ~ 10 裡面隨機挑選一個數字
            audio_index = str(random.randint(1,10))
            # 音訊位址：讓 Vercel 伺服器知道你的音訊位址在哪裡（範例：static/audios/audio1.mp3）
            url = request.url_root + 'static/audios/sound' + audio_index + '.mp3'
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        AudioMessage()
                    ]
                )
            )

        elif text == '我要抽影片':
            # 隨機亂數：從 1 ~ 10 裡面隨機挑選一個數字
            video_index = str(random.randint(1,10))
            # 音訊位址：讓 Vercel 伺服器知道你的音訊位址在哪裡（範例：static/videos/video1.mp4）
            url = request.url_root + 'static/videos/video' + video_index + '.mp4'
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        VideoMessage(original_content_url=url, preview_image_url=url)
                    ]
                )
            )

        elif text == '我要抽位置':
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        # 自訂經緯度座標：標題、地址、經度、緯度
                        LocationMessage(title="台北信義", address="忠孝東路5段68號", latitude=25.033493, longitude=121.564101)
                    ]
                )
            )

if __name__ == "__main__":
    app.run()