from FoodFinder.models import HistoryResult
from FoodFinder.lda import Recommend, preprocess_input, retrieve
from datetime import datetime
from linebot.models import *
from FoodFinder.models import HistoryResult
from django.db.models import Count
import re
# 回傳與關鍵字相似的餐廳


def createPostTemplate(rank_result):
    action_list = []
    if (len(rank_result) == 0):
        action_list.append(PostbackTemplateAction(
            label='沒有與關鍵字類似的餐廳', text='沒有與關鍵字類似的餐廳', data='沒有與關鍵字類似的餐廳'))
    if (len(rank_result) > 0):
        rank1 = re.sub(u"([^\u4e00-\u9fa5])", "", rank_result[0]
                       ) if len(rank_result[0]) > 20 else rank_result[0]
        action_list.append(PostbackTemplateAction(
            label=rank1, text=rank1, data=rank1))
    if (len(rank_result) > 1):
        rank2 = re.sub(u"([^\u4e00-\u9fa5])", "", rank_result[1]
                       ) if len(rank_result[1]) > 20 else rank_result[1]
        action_list.append(PostbackTemplateAction(
            label=rank2, text=rank2, data=rank2))
    if (len(rank_result) > 2):
        rank3 = re.sub(u"([^\u4e00-\u9fa5])", "", rank_result[2]
                       ) if len(rank_result[2]) > 20 else rank_result[2]
        action_list.append(PostbackTemplateAction(
            label=rank3, text=rank3, data=rank3))
    if (len(rank_result) > 3):
        rank4 = re.sub(u"([^\u4e00-\u9fa5])", "", rank_result[3]
                       ) if len(rank_result[3]) > 20 else rank_result[3]
        action_list.append(PostbackTemplateAction(
            label=rank4, text=rank4, data=rank4))
    return action_list

# 回傳類似主題餐廳


def createTemplate(selected, recommend_result):
    action_list = []
    if (len(recommend_result) == 0):
        action_list.append(MessageTemplateAction(
            label=selected, text="您的推薦結果: "+selected, data=selected))
    if (len(recommend_result) > 0):
        rec1 = re.sub(u"([^\u4e00-\u9fa5])", "", recommend_result[0]
                      ) if len(recommend_result[0]) > 20 else recommend_result[0]
        action_list.append(MessageTemplateAction(
            label=rec1, text="您的推薦結果: "+rec1, data=rec1))
    if (len(recommend_result) > 1):
        rec2 = re.sub(u"([^\u4e00-\u9fa5])", "", recommend_result[1]
                      ) if len(recommend_result[1]) > 20 else recommend_result[1]
        action_list.append(MessageTemplateAction(
            label=rec2, text="您的推薦結果: "+rec2, data=rec2))
    if (len(recommend_result) > 2):
        rec3 = re.sub(u"([^\u4e00-\u9fa5])", "", recommend_result[2]
                      ) if len(recommend_result[2]) > 20 else recommend_result[2]
        action_list.append(MessageTemplateAction(
            label=rec3, text="您的推薦結果: "+rec3, data=rec3))
    if (len(recommend_result) > 3):
        rec4 = re.sub(u"([^\u4e00-\u9fa5])", "", recommend_result[3]
                      ) if len(recommend_result[3]) > 20 else recommend_result[3]
        action_list.append(MessageTemplateAction(
            label=rec4, text="您的推薦結果: "+rec4, data=rec4))
    return action_list


def SaveData(text):
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y")
    HistoryResult.objects.create(
        restaurant_name=text, date=date_time
    )
    print("儲存成功")


def mostRecommend():
    # order_by('-total') = order by DESC
    result = HistoryResult.objects.all().values('restaurant_name').annotate(
        total=Count('restaurant_name')).order_by('-total')
    print(result)
    return result[0].get('restaurant_name') if len(result) > 0 else "沒有推薦結果"


def rankingRestaurant(keyword):
    input_vector = preprocess_input(keyword)
    top_relevant = retrieve(input_vector)
    return top_relevant


def recommendRestaurant(selected_restaurant):
    recommended_restaurants = Recommend(selected_restaurant)
    print(recommended_restaurants)
    return recommended_restaurants
