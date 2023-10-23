
import requests
import json
import time

def add_attendee(first_name, last_name, is_checked_in,email, cookie, token, event_id, chapter_id):
    url = f"https://gdsc.community.dev/api/attendee/?event={event_id}&chapter={chapter_id}"
    payload = "{\"event\":\"" + str(event_id) + "\",\"attendees\":[{\"first_name\":\"" + str(first_name) + "\",\"last_name\":\"" + str(
        last_name) + "\",\"email\":\"" + str(email) + "\",\"is_checked_in\":"+str(is_checked_in).lower()+",\"send_event_email\":true}]}"
    headers = {
        "accept": "application/json; version=bevy.1.0",
        "accept-language": "en",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"117\", \"Google Chrome\";v=\"118\", \"Not=A?Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-csrftoken": str(token),
        "x-requested-with": "XMLHttpRequest",
        "cookie": str(cookie),
        "Referer": "https://gdsc.community.dev/accounts/dashboard/",
        "Referrer-Policy": "same-origin"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    """ sample response:
    [
       {
          "id":1875593,
          "attendee_uuid":"...",
          "attendee_code":"...",
          "first_name":"Zavaar",
          "last_name":"Shah",
          "email":"hh3509@wayne.edu",
          "title":"",
          "company":"",
          "twitter":null,
          "avatar":{
            
          },
          "profile_url":"/u/mc3cgr/",
          "featured":null,
          "event":80600,
          "masked_email":"h*****@wayne.edu",
          "order_id":null,
          "discount_code":null,
          "user":{
             "id":1188554,
             "first_name":"Zavaar",
             "last_name":"Shah",
             "username":"mc3cgr",
             "email":"h*****@wayne.edu"
          },
          "user_id":1188554,
          "chapter_member_id":null,
          "created_date":"2023-10-23T19:29:28.589739Z",
          "checkin_date":null,
          "deleted_date":null,
          "paid_price":null,
          "paid_currency":null,
          "ticket_title":null,
          "ticket_audience_type_enum_value":null,
          "is_checked_in":false,
          "status":"registered",
          "origin_app":"",
          "event_chapter_id":2871,
          "cohost_registration_chapter":null,
          "cohost_registration_chapter_title":null,
          "name":"Zavaar Shah"
       }
    ]
    """
    if response.status_code >= 200 and response.status_code < 300:
        person = json.loads(response.text)[0]
        print(f"Successfully added: {person['first_name']} {person['last_name']}")
    else:
        print(f"Error adding: {email}\n{response.text}")


def main():
    config_json = json.loads(open("config.json", "r").read())
    cookie = "; ".join([str(x)+"="+str(y) for x,y in config_json["cookie"].items()])
    attendees = open("attendees.txt", "r").read().split("\n")
    start_time = time.time()
    for attendee in attendees:
        if attendee == "":
            continue
        try:
            row = attendee.split(",")
            first_name = row[0]
            last_name = row[1]
            email = row[2]
            add_attendee(first_name=first_name, last_name=last_name, email=email, is_checked_in=True,
                    cookie=cookie, token=config_json["cookie"]["csrftoken"], event_id=config_json["event_id"], chapter_id=config_json["chapter_id"])
        except Exception as e:
            print(f"Error adding: {attendee}\n{e}")
        finally:
            print("-"*50)
    print(f"Time taken: {int(time.time()-start_time)} seconds")
    
main()
    