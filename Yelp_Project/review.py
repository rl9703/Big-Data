import pymysql
import os,json

file = os.path.abspath('D:\yelp-dataset\yelp_academic_dataset_review.json')
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
    review_id = val(item.get("review_id", None))
    user_id = val(item.get("user_id", None))
    business_id = val(item.get("business_id", None))
    review_stars = val(item.get("stars", None))
    review_date = val(item.get("date", None))
    review_text = val(item.get("text", None))
    review_useful = val(item.get("useful", None))
    review_funny = val(item.get("funny", None))
    review_cool = val(item.get("cool", None))

    try:
        cursor.execute('INSERT INTO Review(review_id,'
                       'business_id,'
                       'user_id,review_cool,'
                       'review_date,review_funny, review_stars,review_useful,review_text )'
                       ' VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s)',
                       (review_id, business_id, user_id, review_cool,
                       review_date, review_funny, review_stars,
                       review_useful, review_text))
        con.commit()
    except Exception as e:
        print(e)
        con.commit()
    print("Done", i)
con.commit()
con.close()