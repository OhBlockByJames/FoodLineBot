from FoodFinder.models import HistoryResult
from FoodFinder.lda import Recommend, preprocess_input, retrieve
from datetime import datetime
# from FoodFinder.models import HistoryResult


def Greeting():
    text = '此帳號會將餐廳推薦給您 \n 輸入格式範例 \n [推薦] 叉燒 日式 拉麵 柑橘'
    return text


def SaveData(text):
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y")
    HistoryResult.objects.create(
        restaurant_name=text, date=date_time
    )
    print("儲存成功")


def rankingRestaurant(keyword):
    input_vector = preprocess_input(keyword)
    top_relevant = retrieve(input_vector)
    return top_relevant


def recommendRestaurant(selected_restaurant):
    recommended_restaurants = Recommend(selected_restaurant)
    return recommended_restaurants
