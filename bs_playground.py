from bs4 import BeautifulSoup
import re
from rule import parseTitle

html_content = """
<div class="item">
<div class="pic">
    <em>3</em>
    <a href="https://movie.douban.com/subject/1292722/">
        <img width="100" alt="泰坦尼克号" src="https://img9.doubanio.com/view/photo/s_ratio_poster/public/p457760035.jpg">
    </a>
</div>
<div class="info">
    <div class="hd">
        <a href="https://movie.douban.com/subject/1292722/">
            <span class="title">泰坦尼克号</span>
                    <span class="title">&nbsp;/&nbsp;Titanic</span>
                <span class="other">&nbsp;/&nbsp;铁达尼号(港 / 台)</span>
        </a>


            <span class="playable">[可播放]</span>
    </div>
    <div class="bd">
        <p>
            导演: 詹姆斯·卡梅隆 James Cameron&nbsp;&nbsp;&nbsp;主演: 莱昂纳多·迪卡普里奥 Leonardo...<br>
            1997&nbsp;/&nbsp;美国 墨西哥&nbsp;/&nbsp;剧情 爱情 灾难
        </p>

        
        <div>
            <span class="rating5-t"></span>
            <span class="rating_num" property="v:average">9.5</span>
            <span property="v:best" content="10.0"></span>
            <span>2390916人评价</span>
        </div>

            <p class="quote">
                <span>失去的才是永恒的。 </span>
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
print(parseTitle(soup))
