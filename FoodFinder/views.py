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
                    if "[推薦]" in input:
                        input = input.replace("[推薦] ", "")
                        rank_result = rankingRestaurant(input)
                        rank1 = rank_result[0] if len(
                            rank_result) > 0 else '沒有與關鍵字類似的餐廳'
                        rank2 = rank_result[1] if len(
                            rank_result) > 1 else '沒有與關鍵字類似的餐廳'
                        rank3 = rank_result[2] if len(
                            rank_result) > 2 else '沒有與關鍵字類似的餐廳'
                        rank4 = rank_result[3] if len(
                            rank_result) > 3 else '沒有與關鍵字類似的餐廳'
                        reply_arr.append(
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    title='與關鍵字類似的餐廳',
                                    text='選擇您的餐廳偏好',
                                    actions=[
                                        PostbackTemplateAction(
                                            label=rank1,
                                            text=rank1,
                                            data=rank1
                                        ),
                                        PostbackTemplateAction(
                                            label=rank2,
                                            text=rank2,
                                            data=rank2
                                        ),
                                        PostbackTemplateAction(
                                            label=rank3,
                                            text=rank3,  # 按下後輸入的文字
                                            data=rank3
                                        ),
                                        PostbackTemplateAction(
                                            label=rank4,
                                            text=rank4,  # 按下後輸入的文字
                                            data=rank4
                                        )
                                    ]
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
                                    text='輸入格式範例 \n [推薦] 叉燒 日式 拉麵 柑橘',
                                    actions=[
                                        MessageTemplateAction(
                                            label='開始使用',
                                            text='請輸入您的關鍵字',
                                        ),
                                        MessageTemplateAction(
                                            label='我都可以',
                                            text='我都可以',
                                        ),
                                    ]
                                )
                            )
                        )
                    elif "我都可以" in input:
                        print('我都可以')
                    elif "您的推薦結果: 沒有類似主題的餐廳" in input:
                        reply_arr = []
                        reply_arr.append(TextSendMessage(
                            text="無法推薦餐廳給您 我們深感遺憾..."))
                        reply_arr.append(StickerSendMessage(
                            package_id=11539, sticker_id=52114110))
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            reply_arr
                        )
                    elif "您的推薦結果:" in input:
                        insert = input.replace("您的推薦結果: ", "")
                        print(insert)
                        SaveData(insert)
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            TextSendMessage(text="感謝您的使用!!!")
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
                        event.reply_token, ImageSendMessage(original_content_url='https://i.imgur.com/34MoctZ.jpg', preview_image_url='https://i.imgur.com/34MoctZ.jpg'))  # 原圖/縮圖
            elif isinstance(event, PostbackEvent):  # 如果有回傳值事件
                if event.postback.data != '沒有與關鍵字類似的餐廳':
                    selected = event.postback.data
                    recommend_result = recommendRestaurant(selected)
                    print(recommend_result)
                    rec1 = recommend_result[0] if len(
                        recommend_result) > 0 else selected
                    rec2 = recommend_result[1] if len(
                        recommend_result) > 1 else '沒有類似主題的餐廳'
                    rec3 = recommend_result[2] if len(
                        recommend_result) > 2 else '沒有類似主題的餐廳'
                    rec4 = recommend_result[3] if len(
                        recommend_result) > 3 else '沒有類似主題的餐廳'
                    line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='Menu',
                                text='請選擇美食類別',
                                actions=[
                                    MessageTemplateAction(
                                        label=rec1,
                                        text="您的推薦結果: "+rec1,
                                    ),
                                    MessageTemplateAction(
                                        label=rec2,
                                        text="您的推薦結果: "+rec2,
                                    ),
                                    MessageTemplateAction(
                                        label=rec3,
                                        text="您的推薦結果: "+rec3,
                                    ),
                                    MessageTemplateAction(
                                        label=rec4,
                                        text="您的推薦結果: "+rec4,
                                    ),
                                ]
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
