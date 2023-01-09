from FoodFinder.models import HistoryResult
from FoodFinder.lda import Recommend, preprocess_input, retrieve
from datetime import datetime
from linebot.models import *
from FoodFinder.models import HistoryResult
from django.db.models import Count

# 回傳與關鍵字相似的餐廳


def createPostTemplate(rank_result):
    action_list = []
    if (len(rank_result) == 0):
        action_list.append(PostbackTemplateAction(
            label='沒有與關鍵字類似的餐廳', text='沒有與關鍵字類似的餐廳', data='沒有與關鍵字類似的餐廳'))
    if (len(rank_result) > 0):
        action_list.append(PostbackTemplateAction(
            label=rank_result[0], text=rank_result[0], data=rank_result[0]))
    if (len(rank_result) > 1):
        action_list.append(PostbackTemplateAction(
            label=rank_result[1], text=rank_result[1], data=rank_result[1]))
    if (len(rank_result) > 2):
        action_list.append(PostbackTemplateAction(
            label=rank_result[2], text=rank_result[2], data=rank_result[2]))
    if (len(rank_result) > 3):
        action_list.append(PostbackTemplateAction(
            label=rank_result[3], text=rank_result[3], data=rank_result[3]))
    return action_list

# 回傳類似主題餐廳


def createTemplate(selected, recommend_result):
    action_list = []
    if (len(recommend_result) == 0):
        action_list.append(MessageTemplateAction(
            label=selected, text="您的推薦結果: "+selected, data=selected))
    if (len(recommend_result) > 0):
        action_list.append(MessageTemplateAction(
            label=recommend_result[0], text="您的推薦結果: "+recommend_result[0], data=recommend_result[0]))
    if (len(recommend_result) > 1):
        action_list.append(MessageTemplateAction(
            label=recommend_result[1], text="您的推薦結果: "+recommend_result[1], data=recommend_result[1]))
    if (len(recommend_result) > 2):
        action_list.append(MessageTemplateAction(
            label=recommend_result[2], text="您的推薦結果: "+recommend_result[2], data=recommend_result[2]))
    if (len(recommend_result) > 3):
        action_list.append(MessageTemplateAction(
            label=recommend_result[3], text="您的推薦結果: "+recommend_result[3], data=recommend_result[3]))
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
    return recommended_restaurants
