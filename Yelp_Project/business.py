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

for i, item in enumerate(json_obj):

    business_id = val(item.get("business_id", None))
    name = val(item.get("name", None))
    address = val(item.get("address", None))
    city = val(item.get("city", None))
    state = val(item.get("state", None))
    postal_code = val(item.get("postal_code", None))
    latitude = val(item.get("latitude", None))
    longitude = val(item.get("longitude", None))
    is_open = val(item.get("is_open", None))

    cursor.execute('INSERT INTO Business(business_id,'
                   'business_name,'
                   'business_address,'
                   'business_state,'
                   'business_city,'
                   'business_is_open,'
                   ' business_latitude,'
                   'business_longitude,'
                   ' business_postal_code)'
                   ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                   (business_id, name, address, state, city, is_open, latitude, longitude, postal_code))
    print("Done", i)
con.commit()
con.close()