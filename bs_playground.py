from bs4 import BeautifulSoup
import re

html_content = """
<div class="item">
    <div class="pic">
        <em class="">4</em>
        <a href="https://movie.douban.com/subject/1292722/">
            <img width="100" alt="泰坦尼克号" src="https://img9.doubanio.com/view/photo/s_ratio_poster/public/p457760035.jpg" class="">
        </a>
    </div>
    <div class="info">
        <div class="hd">
            <a href="https://movie.douban.com/subject/1292722/" class="">
                <span class="title">泰坦尼克号</span>
                        <span class="title">&nbsp;/&nbsp;Titanic</span>
                    <span class="other">&nbsp;/&nbsp;铁达尼号(港 / 台)</span>
            </a>
            <span class="playable">[可播放]</span>
        </div>
        <div class="bd">
            <p class="">
                导演: 詹姆斯·卡梅隆 James Cameron&nbsp;&nbsp;&nbsp;主演: 莱昂纳多·迪卡普里奥 Leonardo...<br>
                1997&nbsp;/&nbsp;美国 墨西哥&nbsp;/&nbsp;剧情 爱情 灾难
            </p>
            <div class="star">
                    <span class="rating5-t"></span>
                    <span class="rating_num" property="v:average">9.5</span>
                    <span property="v:best" content="10.0"></span>
                    <span>2275180人评价</span>
            </div>
            <p class="quote">
                <span class="inq">失去的才是永恒的。 </span>
            </p>
            <p>
                <span class="gact">
                <a href="https://movie.douban.com/wish/45046660/update?add=1292722" target="_blank" class="j a_collect_btn" name="sbtn-1292722-wish" rel="nofollow">想看</a>
                </span>&nbsp;&nbsp;
            </p>
        </div>
    </div>
</div>
"""

soup = BeautifulSoup(html_content, "html.parser")

pattern = re.compile(r"/(?![^(]*\))")


def parseTitle(element):
    othername = []
    cn_title = ""
    en_title = ""

    # Find all 'a' tags with class '' (empty class in the example)
    for a_tag in element.find_all("a", class_=""):
        # Find all 'span' with class 'title' within each 'a' tag
        titles = a_tag.find_all("span", class_="title")
        # Extract text and strip it to clean up whitespace
        # first is Chinese name, second is english name, replace '/' to avoid confusion
        for index, elm in enumerate(titles):
            # if title contains "(港 / 台)" treat as one unit and not split by /
            title = elm.text.replace("\xa0", " ").replace("/", "").strip()
            if index == 0:
                cn_title = title
            else:
                en_title = title

        other_titles = a_tag.find("span", class_="other")
        if other_titles:
            alternative_names = [
                name.strip()
                for name in pattern.split(other_titles.text)
                if name.strip()
            ]
            othername.extend(alternative_names)

    # Print the list of film names and alternative names
    othername = [s.replace("\xa0", " ").strip() for s in othername]
    othername = list(filter(lambda x: x != "", othername))
    return [cn_title, en_title, othername]


print(parseTitle(soup))
