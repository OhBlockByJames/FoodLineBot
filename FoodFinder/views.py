from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from FoodFinder.functions import *

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
                    if "keywords" in input:
                        input = input.replace("keywords", "")
                        input = input.strip()
                        rank_result = rankingRestaurant(input)
                        action_list = createPostTemplate(rank_result)
                        reply_arr.append(
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    title='與關鍵字類似的餐廳',
                                    text='選擇您的餐廳偏好',
                                    actions=action_list
                                )
                            )
                        )
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            reply_arr
                        )
                    elif "嗨" in input:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    title='歡迎使用',
                                    text='輸入格式範例 \n keywords 叉燒 日式 拉麵 柑橘',
                                    actions=[
                                        MessageTemplateAction(
                                            label='開始使用',
                                            text='請輸入您的關鍵字',
                                        ),
                                        MessageTemplateAction(
                                            label='隨便~都可以~',
                                            text='隨便~都可以~',
                                        ),
                                    ]
                                )
                            )
                        )
                    elif "隨便~都可以~" in input:
                        reply_arr = []
                        result = mostRecommend()
                        msg = getLink(result)
                        reply_arr.append(TextSendMessage(
                            text="您的推薦結果: "+result))
                        reply_arr.append(TextSendMessage(
                            text=msg))
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            reply_arr
                        )
                    elif "您的推薦結果:" in input:
                        insert = input.replace("您的推薦結果: ", "")
                        SaveData(insert)
                        msg = getLink(insert)
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
                else:  # 其他
                    line_bot_api.reply_message(
                        event.reply_token, ImageSendMessage(original_content_url='https://api.jikipedia.com/upload/2524fa82bf0c30887ae202d45bb90356_scaled.jpg', preview_image_url='https://api.jikipedia.com/upload/2524fa82bf0c30887ae202d45bb90356_scaled.jpg'))  # 原圖/縮圖
            elif isinstance(event, PostbackEvent):  # 如果有回傳值事件
                if event.postback.data != '沒有與關鍵字類似的餐廳':
                    selected = event.postback.data
                    recommend_result = recommendRestaurant(selected)
                    action_list = createTemplate(selected, recommend_result)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='餐廳推薦結果',
                                text='請選擇您的推薦結果',
                                actions=action_list
                            )
                        )
                    )
                else:
                    reply_arr = []
                    reply_arr.append(TextSendMessage(text="我不知道您想表達什麼..."))
                    reply_arr.append(StickerSendMessage(
                        package_id=11539, sticker_id=52114110))
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        reply_arr
                    )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
