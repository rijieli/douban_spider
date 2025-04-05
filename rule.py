from bs4 import BeautifulSoup
import re

pattern = re.compile(r"/(?![^(]*\))")


def parseTitle(element):
    othername = []
    cn_title = ""
    en_title = ""

    # Find all 'a' tags with class '' (empty class in the example)
    for a_tag in element.find_all("div", class_="hd"):
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
