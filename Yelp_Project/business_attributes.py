import pymysql
import os,json
import ast

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
            if value == "False" or value == "None":
                return False
            elif value == "True":
                return True
            else:
                return value


con = pymysql.connect(host='localhost', user='root', passwd='Skywalker@1993', db='yelpDB')
cursor = con.cursor()

for i, item in enumerate(json_obj):

    business_id = val(item.get("business_id", None))
    attributes = item.get("attributes", None)
    if attributes is not None:
        busines_parking = attributes.get("BusinessParking", None)
        if busines_parking is not None:
            busines_parking = ast.literal_eval(busines_parking)
            if type(busines_parking) is dict:
                garage_parking = val(busines_parking.get("garage", False))
                street_parking = val(busines_parking.get("street", False))
                valet_parking = val(busines_parking.get("valet", False))
                parking_lot = val(busines_parking.get("lot", False))
        else:
            garage_parking = False
            street_parking = False
            valet_parking = False
            parking_lot = False

        bike_parking = val(attributes.get("BikeParking", False))
        business_accepts_bitcoin = val(attributes.get("BusinessAcceptsBitcoin", False))
        business_accepts_creditcard = val(attributes.get("BusinessAcceptsCreditCards", False))
        dogs_allowed = val(attributes.get("DogsAllowed", False))
        price_range = val(attributes.get("RestaurantsPriceRange2", 0))
        wheelchair_access = val(attributes.get("WheelchairAccessible", False))

        cursor.execute('INSERT INTO Business_attributes(business_id,'
                       'bike_parking,'
                       'business_accepts_bitcoin,'
                       'business_accepts_creaditcard,'
                       'garage_parking,'
                       'street_parking,'
                       'dogs_allowed,'
                       'price_range, wheelchair_access,valet_parking,'
                       ' parking_lot)'
                       ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)',
                       (business_id, bike_parking, business_accepts_bitcoin, business_accepts_creditcard,
                        garage_parking, street_parking, dogs_allowed, price_range,
                        wheelchair_access, valet_parking, parking_lot))
    print("Done", i)
con.commit()
con.close()