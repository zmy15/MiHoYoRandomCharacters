import os
import requests
from api import Api


def Update_StarRail_Json() -> bool:
    if not os.path.exists("update.txt"):
        with open("update.txt", "w", encoding="utf-8") as f:
            f.write("")
    with open("update.txt", "r", encoding="utf-8") as f:
        StarRail_Update_Oldinfo = f.read()
    try:
        StarRail_Update_data = requests.get(Api.StarRail_Update).json()
        try:
            if StarRail_Update_data.get("message").startswith("API"):
                print("检查更新次数过于频繁！访问被限制")
                return False
        except Exception as e:
            pass
        StarRail_Update_info = StarRail_Update_data[0]["sha"]
    except Exception as e:
        print(e)
        print("检查更新失败！请尝试更换网络！")
        return False
    if StarRail_Update_info != StarRail_Update_Oldinfo:
        with open("update.txt", "w", encoding="utf-8") as f:
            f.write(StarRail_Update_info)
        return True
    else:
        return False
