import os
import requests
import json
import time
from tqdm import tqdm
from api import Api

requests_header_StarRail = {
    "referer": "https://sr.yatta.moe/cn/archive/avatar",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
}
requests_header_Genshin = {
    "referer": "https://gi.yatta.moe/chs/archive/avatar",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
}


def Download_StarRail_Json():
    StarRail_Json_Url = Api.StarRail_Json_Url
    try:
        status_code = requests.get(StarRail_Json_Url).status_code
        if status_code in [403, 404, 502]:
            print("下载请求次数过多，请尝试更换网络或开启代理！")
            return
        Characters_datas = requests.get(StarRail_Json_Url).json()
        for Characters_data in Characters_datas["data"]["items"].items():
            Characters_number = Characters_data[0]
            if Characters_number in ["1001", "1224", "8001", "8002", "8003", "8004", "8005", "8006"]:
                if Characters_number == "1001":
                    Characters_data[1]["name"] = "三月七·存护"
                elif Characters_number == "1224":
                    Characters_data[1]["name"] = "三月七·巡猎"
                elif Characters_number in ["8001", "8002"]:
                    Characters_data[1]["name"] = "开拓者·毁灭"
                elif Characters_number in ["8003", "8004"]:
                    Characters_data[1]["name"] = "开拓者·存护"
                elif Characters_number in ["8005", "8006"]:
                    Characters_data[1]["name"] = "开拓者·同谐"
        with open("StarRail.json", "w", encoding="utf-8") as f:
            json.dump(Characters_datas, f, ensure_ascii=False, indent=4)
            print("星铁角色信息文件下载成功！")
    except Exception as e:
        print(e)
        print("下载星铁角色信息文件失败，请尝试更换网络或开启代理")


def Download_StarRail_Image():
    StarRail_Image_Baseurl = Api.StarRail_Image_Baseurl
    with open("StarRail.json", "r", encoding="utf-8") as f:
        Characters_datas = json.load(f)
    for Characters_data in Characters_datas["data"]["items"].items():
        Characters_Name = Characters_data[1]["name"]
        Characters_number = Characters_data[0]
        StarRail_Image_Url = StarRail_Image_Baseurl + Characters_number + ".png?vh=2024120200"
        Characters_FileName = os.path.join("./StarRail_Image", Characters_Name + ".png")
        if not os.path.exists("./StarRail_Image"):
            os.makedirs("./StarRail_Image")
        if os.path.exists(Characters_FileName):
            print(f"{Characters_Name}角色图片存在，跳过下载!")
            continue
        try:
            StarRail_Image = requests.get(StarRail_Image_Url, headers=requests_header_StarRail, stream=True)
            total_size = int(StarRail_Image.headers.get('content-length', 0))
            with open(Characters_FileName, 'wb') as file, tqdm(
                    desc=Characters_FileName,
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
            ) as bar:
                for chunk in StarRail_Image.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        bar.update(len(chunk))
                time.sleep(0.8)
        except Exception as e:
            print(e)
            print("下载星铁角色图片失败，请尝试更换网络或开启代理")


def Download_Genshin_Json():
    Genshin_Image_Data = requests.get(Api.Genshin_Json_Url, headers=requests_header_Genshin).json()
    items_data = Genshin_Image_Data.get("data", {}).get("items", {})
    try:
        with open("Genshin.json", "w", encoding="utf-8") as f:
            json.dump(items_data, f, ensure_ascii=False, indent=4)
            print("原神角色信息文件下载成功！")
    except Exception as e:
        print(e)
        print("下载原神角色信息文件失败，请尝试更换网络或开启代理")


def Download_Genshin_Image():
    with open("Genshin.json", "r", encoding="utf-8") as f:
        Genshin_Image_Data = json.load(f)
    for item in Genshin_Image_Data.values():
        Characters_id = item["icon"]
        Characters_Name = item["name"]
        Genshin_ImagUrl = Api.Genshin_Image_Baseurl + Characters_id + ".png?vh=2024100700"
        Characters_FileName = os.path.join("./Genshin_Image", Characters_Name + ".png")
        if not os.path.exists("./Genshin_Image"):
            os.makedirs("./Genshin_Image")
        if os.path.exists(Characters_FileName):
            print(f"{Characters_Name}角色图片存在，跳过下载!")
            continue
        Genshin_Image = requests.get(Genshin_ImagUrl, headers=requests_header_StarRail, stream=True)
        total_size = int(Genshin_Image.headers.get('content-length', 0))
        with open(Characters_FileName, 'wb') as file, tqdm(
                desc=Characters_FileName,
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for chunk in Genshin_Image.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    bar.update(len(chunk))
            time.sleep(0.6)


if __name__ == "__main__":
    RED = "\033[31m"
    RESET = "\033[0m"
    print(
        f"{RED}如果出现权限不足(Permission denied)无法下载，请以管理员权限运行或安装到其他位置！{RESET}")
    try:
        Download_StarRail_Json()
        Download_StarRail_Image()
        Download_Genshin_Json()
        Download_Genshin_Image()
    except Exception as e:
        print(e)
        os.system("pause")
