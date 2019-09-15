import pymysql
import os,json

file = os.path.abspath('D:\yelp-dataset\yelp_academic_dataset_business.json')
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

cateogry = []
for i, item in enumerate(json_obj):

    cat = val(item.get("categories", None))
    business_id = val(item.get("business_id", None))
    if cat is not None:
        cat = str(cat)
        cat = cat.split(",")
        for k in cat:
            k = k.strip()
            if k not in cateogry:
                cateogry.append(k)
                catId = (cateogry.index(k)+1)
                cursor.execute('INSERT INTO Category (category_id, category_name)VALUES (%s, %s)', (catId, k))
            catId = (cateogry.index(k) + 1)
            cursor.execute('INSERT INTO Business_Category (business_id, category_id)VALUES (%s, %s)', (business_id, catId))
    print("Done", i)
con.commit()
con.close()