from flask import Flask
from config.mongoConnection import raw_data_collecction
from datetime import date

def get_rawdata(look_date):
    today = date.today()
    if look_date:
        try:
            data = raw_data_collecction.find_one(
                {
                    "date": look_date
                }
            )
            return data
        except Exception as e:
            print("Error in getting data : ",e)
            return False
    else:
        data = raw_data_collecction.find_one(
            {
                "date": today
            }
        )
        return data

