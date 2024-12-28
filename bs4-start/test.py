from bs4 import BeautifulSoup
# import lxml

with open("website.html") as website_file:
    contents = website_file.read()

soup = BeautifulSoup(contents, "html.parser")
#Equivalent to
# soup = BeautifulSoup(contents, "lxml")

# print(soup.title)
# print(soup.title.string)
#
# print(soup.prettify())

# print(soup.li)

all_anchor_tags = soup.find_all(name="a")
# print(*all_anchor_tags, sep="\n")

# for tag in all_anchor_tags:
#     # print(tag.getText())
#     print(tag.get("href"))

# heading = soup.find(name="h1", id="name")
# print(heading)
#
# section_heading = soup.find(name="h3", class_="heading")
# print(section_heading.getText())
# print(section_heading.name)
# print(section_heading.get("class"))

company_url = soup.select_one(selector="p a")
print(company_url.get("href"))
print(company_url.getText())

# headings = soup.select(".heading")
# print(*headings, sep="\n")