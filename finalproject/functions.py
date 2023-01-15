import random
import pandas as pd
import math
from .config import DB_ENGINE
from .models import Profile, Prediction

def calculate_score(request):
    #x = random.randint(10,100)
    #request["profile"].score = 100
    #request["profile"].save()
    #print("RANDOM NUMBER", x)
    #print("PROFILE: ", request["profile"].profile_name)
    #print("STOCK: ", request["selected_stock"])

    #user_profile = Profile.objects.get(profile_name=request["profile"].profile_name)
    try:
        user_name = request["profile"].profile_name
        user_score = request["profile"].score

        stock_bought_ok = 0
        stock_sold_ok = 0
        stock_bought = 0
        stock_sold = 0

        selected_stock = request["selected_stock"]
        buy_price = float(request["buy_price"])
        sell_price = float(request["sell_price"])
        money_amount = float(request["money_amount"])

        prediction_restricted = 0

    #print("selected stock:", type(selected_stock))
    #print("buy price:", type(buy_price))
    #print("sell price:", type(sell_price))
    #print("money amount:", type(money_amount))

        stock_df = pd.read_sql("select distinct * from stock_prices where stock_name='{stock_name}'".format(stock_name=selected_stock), DB_ENGINE)
        stock_high = stock_df["High"].tolist()
        stock_low = stock_df["Low"].tolist()
        stock_open = stock_df["Open"].tolist()
        stock_close = stock_df["Close"].tolist()

        if(sell_price < buy_price):
            prediction_restricted = 1

        if (buy_price > stock_open[0]):
            buy_price = stock_open[0]

        if (sell_price < stock_open[0]):
            sell_price = stock_open[0]

        if(money_amount > user_score):
            money_amount = user_score

        if prediction_restricted == 0:
            for i in range(len(stock_low)):
                if stock_low[i] <= buy_price:
                    stock_bought_ok = 1
                    #stock_bought = int(math.floor(money_amount / buy_price))
                    stock_bought = money_amount / buy_price
                    user_score = user_score - (stock_bought * buy_price)
                    break
            
            for i in range(len(stock_high)):
                if stock_bought_ok == 1:
                    if stock_high[i] >= sell_price:
                        stock_sold_ok = 1
                        stock_sold = stock_bought
                        user_score = user_score + (stock_sold * sell_price)
                        break
            
            if stock_bought_ok == 1 and stock_sold_ok == 0:
                user_score = user_score + (stock_bought * stock_close[len(stock_close)-1])
        
        user_score = float("{:.2f}".format(user_score))

        request["profile"].score = user_score
        request["profile"].save()
    except:
        pass

