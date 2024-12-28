from bs4 import BeautifulSoup
import requests

response = requests.get("https://news.ycombinator.com/news")
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, "html.parser")

# article_tag = soup.find(name="span", class_="titleline")
# article_text = article_tag.getText()
# article_link = article_tag.get("href")
# article_upvote = soup.find(name="span", class_="score").getText()

# print(article_text)
# print(article_tag)
# print(f"Link: {article_link}")
# print(article_upvote)


#Articles
articles = soup.find_all(name="span", class_="titleline")
article_texts = []
article_links = []

for article_tag in articles:
    text = article_tag.getText()
    article_texts.append(text)
    link = article_tag.find("a").get("href")
    article_links.append(link)

article_upvotes = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]

# print(article_texts)
# print(article_links)
# print(article_upvotes)

# highest_vote = 0
# highest_vote_article = None
# highest_vote_article_text = None
#
# for vote_index in range(len(article_upvotes)):
#     vote = article_upvotes[vote_index]
#
#     if vote > highest_vote:
#         highest_vote = vote
#         highest_vote_article = article_links[vote_index]
#         highest_vote_article_text = article_texts[vote_index]
#
# print(highest_vote_article_text)
# print(highest_vote_article)
# print(highest_vote)

largest_number = max(article_upvotes)
largest_index = article_upvotes.index(largest_number)

print(article_texts[largest_index])
print(article_links[largest_index])
print(largest_number)