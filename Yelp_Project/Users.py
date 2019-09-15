import pymysql
import os,json

file = os.path.abspath('D:\yelp-dataset\yelp_academic_dataset_user.json')
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
    user_name = val(item.get("name", None))
    user_since = val(item.get("yelping_since", None))

    cursor.execute('INSERT INTO Users(user_id,user_name,user_since) VALUES (%s, %s, %s)',
                   (user_id, user_name, user_since))
    print("Done", i)
con.commit()
con.close()