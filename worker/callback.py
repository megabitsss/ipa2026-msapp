from datetime import datetime
from bson import json_util
from router_client import get_interfaces

# Preparing for saving the SSH result to database
from pymongo import MongoClient
import os

mongo_uri = os.environ.get("MONGO_URI", "mongodb://127.0.0.1:27017/")
db_name = os.environ.get("DB_NAME", "ipa2026_db")
client = MongoClient(mongo_uri)
db = client[db_name]
collection = db["routers"]


def callback(ch, method, props, body):
    job = json_util.loads(body.decode())
    router_ip = job["ip"]
    router_username = job["username"]
    router_password = job["password"]
    print(f"Received job for router {router_ip}")

    try:
        result = get_interfaces(router_ip, router_username, router_password)
        if result:
            collection.update_one(
                {
                    "ip": router_ip
                },
                {
                    "$push": {
                        "history": {
                            "timestamp": datetime.now(),
                            "interfaces": result
                        }
                    }
                },
                # ถ้ายังไม่มี IP นี้ใน DB ให้สร้าง Document ใหม่ตั้งต้นให้เลย
                upsert=True,
            )
            print(f" เพิ่มประวัติ interfaces ของ {router_ip}"
                " ลงใน history สำเร็จ!"
            )
        else:
            print(f" ไม่พบข้อมูล interfaces จาก {router_ip}")
    except Exception as e:
        print(f" Error: {e}")
