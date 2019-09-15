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
    friends = val(item.get("friends", None))
    if friends is not None:
        friends = str(friends)
        friend_list = friends.split(",")
        for k in friend_list:
            k = k.strip()
            cursor.execute('INSERT INTO Users_relationships(user1_id, user2_id) VALUES (%s, %s)',
                           (user_id, k))
    print("Done", i)
con.commit()
con.close()