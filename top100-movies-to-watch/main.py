import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇

response = requests.get(URL)
empire_online_web_page = response.text

soup = BeautifulSoup(empire_online_web_page, "html.parser")
movies = soup.find_all(name="h3", class_="title")
movies_list = [movie.getText() for movie in movies]
movies_list.reverse()

with open("movies.txt", "w", encoding="utf-8") as movies_data:
    for movie in movies_list:
        # movie_index = movies_list.index(movie)
        #
        # if movie_index % 58 == 0:
        #     print(movie)

        movies_data.write(movie + "\n")