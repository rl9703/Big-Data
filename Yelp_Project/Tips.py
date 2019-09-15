import pymysql
import os,json

file = os.path.abspath('D:\yelp-dataset\yelp_academic_dataset_tip.json')
json_obj = []
with open(file, encoding='utf-8') as f:
    for line in f:
        json_obj.append(json.loads(line))


def val(value):
    if value is not None:
        if type(value) is int:
            return int(value)
        else:
            return value


con = pymysql.connect(host='localhost', user='root', passwd='Skywalker@1993', db='yelpDB')
cursor = con.cursor()

for i, item in enumerate(json_obj):
    user_id = val(item.get("user_id", None))
    business_id = val(item.get("business_id", None))
    tip_likes = val(item.get("compliment_count", None))
    tip_date = val(item.get("date", None))
    tip_text = val(item.get("text", None))

    cursor.execute('INSERT INTO Tip (business_id,user_id,tip_date,tip_likes, tip_text) VALUES (%s, %s, %s, %s, %s)',
                   (business_id, user_id, tip_date, tip_likes, tip_text))
    print("Done", i)
con.commit()
con.close()