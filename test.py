# import requests
# from bs4 import BeautifulSoup as BS



# file = open("test.html", encoding="utf-8")

# html = file.read()

# soup = BS(html,'html.parser')

# # container = soup.find('div',{'class':'container'}).find('div',{"class":"navigations-container"})
# # ul_list = container.find('ul',{'class':'menu'})
# # li_list = ul_list.find_all('li')

# # for li in li_list:
# #     print(li.text.strip())


# conetnt = soup.find('div',{"class":"content-container"})
# posts = conetnt.find_all("div",{'class':"post"})
# for post_list in posts:
#     title = post_list.find("h1",{'class':'title'}).text.strip()
    
