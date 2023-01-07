from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from FoodFinder.functions import Recommend

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):

    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                if event.message.type == "text":
                    input = event.message.text
                    reply_arr = []
                    if "吃" in input:
                        reply_arr.append(
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    title='餐廳推薦',
                                    text='有想吃的餐廳類型嗎',
                                    actions=[
                                        PostbackTemplateAction(
                                            label='日式',
                                            text='找日式',
                                            data='日式'
                                        ),
                                        PostbackTemplateAction(
                                            label='義式',
                                            text='找義式',
                                            data='義式'
                                        ),
                                        PostbackTemplateAction(
                                            label='中式/台式',
                                            text='找中式/台式',  # 按下後輸入的文字
                                            data='中式 台式'
                                        ),
                                        PostbackTemplateAction(
                                            label='其他',
                                            text='找其他',  # 按下後輸入的文字
                                            data='其他'
                                        )
                                    ]
                                )
                            )
                        )
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            reply_arr
                        )
                    elif "找" not in input:
                        msg = Recommend(input)
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            TextSendMessage(text=msg)
                        )
                elif event.message.type == "sticker":  # 傳貼圖
                    reply_arr = []
                    reply_arr.append(TextSendMessage(text="我不知道您想表達什麼..."))
                    reply_arr.append(StickerSendMessage(
                        package_id=11539, sticker_id=52114110))
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        reply_arr
                    )
                elif event.message.type == "image":  # 傳圖片
                    line_bot_api.reply_message(
                        event.reply_token, ImageSendMessage(original_content_url='https://i.imgur.com/P6M9s9H.jpeg', preview_image_url='https://i.imgur.com/P6M9s9H.jpeg'))  # 原圖/縮圖
                else:  # 其他
                    line_bot_api.reply_message(
                        event.reply_token, ImageSendMessage(original_content_url='https://i.imgur.com/34MoctZ.jpg', preview_image_url='https://i.imgur.com/34MoctZ.jpg'))  # 原圖/縮圖
            elif isinstance(event, PostbackEvent):  # 如果有回傳值事件
                if event.postback.data == "日式":
                    line_bot_api.reply_message(   # 回復「選擇美食類別」按鈕樣板訊息
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='Menu',
                                text='請選擇美食類別',
                                actions=[
                                    MessageTemplateAction(  # 將第一步驟選擇的地區，包含在第二步驟的資料中
                                        label='拉麵',
                                        text='拉麵',
                                    ),
                                    MessageTemplateAction(
                                        label='壽司',
                                        text='壽司',
                                    ),
                                    MessageTemplateAction(
                                        label='定食',
                                        text='定食',
                                    ),
                                    MessageTemplateAction(
                                        label='隨意',
                                        text='隨意',
                                    )
                                ]
                            )
                        )
                    )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
