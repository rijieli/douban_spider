from bs4 import BeautifulSoup
import re  # 正则表达式，与文字匹配
import urllib.request, urllib.error
import json
from datetime import date
from rule import parseTitle
import pprint

# 创建正则表达式
# 影片链接
findLink = re.compile(r'<a href="(.*?)">')
# 影片图片
findImaSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S   让换行符包含在字符中
# 影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 找到评价人数
findJudge = re.compile(r"<span>(\d*)人评价</span>")
# 找到影片类型
findcountry = re.compile(r"\d{4}(.*)")
# 数字
reNum = re.compile(r"\d+")

BASE_URL = "https://movie.douban.com/top250?start="


# 爬取网页
def getData(date_info):
    datalist = {"date": date_info, "data": []}
    id = 1
    for i in range(0, 10):
        url = BASE_URL + str(i * 25)
        html = requstHTML(url)  # 保存爬取的网页源码

        # 逐一解析数据
        soup = BeautifulSoup(html, "html.parser")

        for item_node in soup.find_all("div", class_="item"):
            # print(item)  # 测试
            data = {"id": id}  # 保存
            item = str(item_node).replace("\xa0", " ")

            # re库正则表达式来查找指定字符串,形成列表

            Link = re.findall(findLink, item)[0]  # 链接
            # https://movie.douban.com/subject/1292434/ get douban id using regex
            data["douban_id"] = re.findall(reNum, Link)[0]

            ImaSrc = re.findall(findImaSrc, item)[0]  # 图片链接
            data["douban_image_link"] = ImaSrc

            title = parseTitle(item_node)
            data["cn_title"] = title[0]
            data["second_title"] = title[1]
            data["other_titles"] = title[2]

            Rating = re.findall(findRating, item)[0]  # 评分
            data["rating"] = Rating

            number_of_rating = re.findall(findJudge, item)[0]  # 评价人数
            data["number_of_rating"] = number_of_rating

            # Find <p class="quote"> inner <span>
            quote = item_node.find("p", class_="quote")
            if quote != None:
                quote = quote.find("span").get_text()
                data["introduction"] = quote.replace("。", "").strip()
            else:
                data["introduction"] = ""

            # Find <div class="bd">
            Bd = item_node.find("div", class_="bd").get_text()

            temp = re.search("[0-9]+.*\/?", Bd).group().split("/")
            year, country, category = temp[0], temp[1], temp[2]  # 得到年份、地区、类型

            data["year"] = year.strip()
            data["region"] = country.strip()
            data["category"] = category.strip()
            # 把处理好的一部电影信息放入datalist
            datalist["data"].append(data)
            id += 1

    return datalist


def requstHTML(url):
    head = {  # 模拟浏览器头部信息，向服务器发送消息
        "User-Agent": " Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 83.0.4103.116Safari / 537.36"
    }  # 告诉浏览器我们接受什么水平的文件内容
    request = urllib.request.Request(url, headers=head)
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 保存数据
def saveData(datalist, savepath):
    with open(savepath, "w", encoding="utf-8") as f:
        json.dump(datalist, f, ensure_ascii=False)


def fetchAndSave():
    date_info = str(date.today().year) + "-" + str(date.today().month)
    datalist = getData(date_info)
    savepath = "douban" + date_info + ".json"
    saveData(datalist, savepath)
    print("Fetched count: " + str(len(datalist["data"])))
    print("Saved to " + savepath)


if __name__ == "__main__":
    fetchAndSave()
