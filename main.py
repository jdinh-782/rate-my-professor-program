import urllib.request as u
from bs4 import BeautifulSoup


prof = input("enter professor name: ")
updated_prof = ""

for i in range(0, len(prof)):
    if prof[i] == ' ':
        updated_prof += "%20"
    else:
        updated_prof += prof[i]

school_id = "&sid=U2Nob29sLTI2NDk="
url = f"https://www.ratemyprofessors.com/search/teachers?query={updated_prof}{school_id}"
print(url)

html = u.urlopen(url).read()
soup = BeautifulSoup(html, 'lxml')
div = soup.find_all("div", "CardName__StyledCardName-sc-1gyrgim-0 cJdVEK")

names_and_ids = dict()
name = ""

href = soup.find_all('a', 'TeacherCard__StyledTeacherCard-syjs0d-0 dLJIlx')
prof_id = ""

if len(href) == 0:
    print("no professors found")
    exit(0)

for i in range(0, len(href)):
    for c in href[i].__str__()[85:]:
        if c == '>':
            prof_id = prof_id[:-1]

            for d in div[i]:
                name += d
            names_and_ids[i] = prof_id
            print(i, '->', name)
            name = ""
            prof_id = ""

            break
        prof_id += c

# for key in names_and_ids:
#     print(key, '->', names_and_ids[key])

# grab input from user to choose professor
index = int(input("\nchoose your professor by entering the numbered index: "))

reviews_url = f"https://www.ratemyprofessors.com/ShowRatings.jsp?tid={names_and_ids[index]}"
print(reviews_url)

html = u.urlopen(reviews_url).read()
soup = BeautifulSoup(html, 'lxml')
div = soup.find_all("div", "Comments__StyledComments-dzzyvm-0 gRjWel")

r = ""
reviews = list()

for i in range(0, len(div)):
    for c in div[i].__str__()[54:]:
        if c == '<':
            reviews.append(r)
            r = ""
            break
        r += c

# removes most helpful rating because it is a duplicate
for review in reviews:
    if reviews[0] == review:
        reviews.pop(0)
        break

# for review in reviews:
#     print(review, '\n')

reviews_qualities = list()
reviews_difficulties = list()
html = u.urlopen(reviews_url).read()
soup = BeautifulSoup(html, 'lxml')
div = soup.find_all("div", "CardNumRating__CardNumRatingNumber-sc-17t4b9u-2")

for i in range(0, len(div)):
    if i % 2 == 0:
        reviews_qualities.append(div[i].__str__()[68:71])
    else:
        reviews_difficulties.append(div[i].__str__()[68:71])

print(f"{len(reviews)}\n")
for i in range(0, len(reviews)):
    print(reviews[i], '\nQuality: ', reviews_qualities[i], '\nDifficulty: ', reviews_difficulties[i], '\n')
