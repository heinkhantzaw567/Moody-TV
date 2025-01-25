from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from .models import User
from django.db import IntegrityError
from openai import OpenAI
import requests
import json
from django.conf import settings
from django.http import JsonResponse
movies_detail =[{'Title': 'Hereditary', 'Year': '2018', 'Rated': 'R', 'Released': '08 Jun 2018', 'Runtime': '127 min', 'Genre': 'Drama, Horror, Mystery', 'Director': 'Ari Aster', 'Writer': 'Ari Aster', 'Actors': 'Toni Collette, Milly Shapiro, Gabriel Byrne', 'Plot': 'A grieving family is haunted by tragic and disturbing occurrences.', 'Language': 'English, Spanish', 'Country': 'United States', 'Awards': '52 wins & 113 nominations total', 'Poster': 'https://m.media-amazon.com/images/M/MV5BNTEyZGQwODctYWJjZi00NjFmLTg3YmEtMzlhNjljOGZhMWMyXkEyXkFqcGc@._V1_SX300.jpg', 'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.3/10'}, {'Source': 'Rotten Tomatoes', 'Value': '90%'}, {'Source': 'Metacritic', 'Value': '87/100'}], 'Metascore': '87', 'imdbRating': '7.3', 'imdbVotes': '404,062', 'imdbID': 'tt7784604', 'Type': 'movie', 'DVD': 'N/A', 'BoxOffice': '$44,069,456', 'Production': 'N/A', 'Website': 'N/A', 'Response': 'True', 'youtubeurl': ['https://www.youtube.com/embed/V6wWKNij_1M'], 'trailortitle': ['Hereditary | Official Trailer HD | A24']}, {'Title': 'The Conjuring', 'Year': '2013', 'Rated': 'R', 'Released': '19 Jul 2013', 'Runtime': '112 min', 'Genre': 'Horror, Mystery, Thriller', 'Director': 'James Wan', 'Writer': 'Chad Hayes, Carey W. Hayes', 'Actors': 'Patrick Wilson, Vera Farmiga, Ron Livingston', 'Plot': 'Paranormal investigators Ed and Lorraine Warren work to help a family terrorized by a dark presence in their farmhouse.', 'Language': 'English, Latin', 'Country': 'United States', 'Awards': '15 wins & 22 nominations total', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMTM3NjA1NDMyMV5BMl5BanBnXkFtZTcwMDQzNDMzOQ@@._V1_SX300.jpg', 'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'}, {'Source': 'Rotten Tomatoes', 'Value': '86%'}, {'Source': 'Metacritic', 'Value': '68/100'}], 'Metascore': '68', 'imdbRating': '7.5', 'imdbVotes': '575,822', 'imdbID': 'tt1457767', 'Type': 'movie', 'DVD': 'N/A', 'BoxOffice': '$137,446,368', 'Production': 'N/A', 'Website': 'N/A', 'Response': 'True', 'youtubeurl': ['https://www.youtube.com/embed/k10ETZ41q5o'], 'trailortitle': ['The Conjuring - Official Main Trailer [HD]']}, {'Title': 'Midsommar', 'Year': '2019', 'Rated': 'R', 'Released': '03 Jul 2019', 'Runtime': '148 min', 'Genre': 'Drama, Horror, Mystery', 'Director': 'Ari Aster', 'Writer': 'Ari Aster', 'Actors': 'Florence Pugh, Jack Reynor, Vilhelm Blomgren', 'Plot': "A couple travels to Northern Europe to visit a rural hometown's fabled Swedish mid-summer festival. What begins as an idyllic retreat quickly devolves into an increasingly violent and bizarre competition at the hands of a pagan cult.", 'Language': 'English, Swedish', 'Country': 'United States, Sweden', 'Awards': '27 wins & 75 nominations', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMzQxNzQzOTQwM15BMl5BanBnXkFtZTgwMDQ2NTcwODM@._V1_SX300.jpg', 'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.1/10'}, {'Source': 'Rotten Tomatoes', 'Value': '83%'}, {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72', 'imdbRating': '7.1', 'imdbVotes': '430,392', 'imdbID': 'tt8772262', 'Type': 'movie', 'DVD': 'N/A', 'BoxOffice': '$27,426,361', 'Production': 'N/A', 'Website': 'N/A', 'Response': 'True', 'youtubeurl': ['https://www.youtube.com/embed/1Vnghdsjmd0'], 'trailortitle': ['MIDSOMMAR | Official Trailer HD | A24']}, {'Title': 'It Follows', 'Year': '2014', 'Rated': 'R', 'Released': '13 Mar 2015', 'Runtime': '100 min', 'Genre': 'Horror, Mystery, Thriller', 'Director': 'David Robert Mitchell', 'Writer': 'David Robert Mitchell', 'Actors': 'Maika Monroe, Keir Gilchrist, Olivia Luccardi', 'Plot': 'A young woman is followed by an unknown supernatural force after a sexual encounter.', 'Language': 'English', 'Country': 'United States', 'Awards': '25 wins & 44 nominations total', 'Poster': 'https://m.media-amazon.com/images/M/MV5BNGZiYWRiYjAtODU0NS00YzAzLTk2MzQtZGVlMzVjM2M3MGQ3XkEyXkFqcGc@._V1_SX300.jpg', 'Ratings': [{'Source': 'Internet Movie Database', 'Value': '6.8/10'}, {'Source': 'Rotten Tomatoes', 'Value': '95%'}, {'Source': 'Metacritic', 'Value': '83/100'}], 'Metascore': '83', 'imdbRating': '6.8', 'imdbVotes': '282,689', 'imdbID': 'tt3235888', 'Type': 'movie', 'DVD': 'N/A', 'BoxOffice': '$14,674,076', 'Production': 'N/A', 'Website': 'N/A', 'Response': 'True', 'youtubeurl': ['https://www.youtube.com/embed/HkZYbOH0ujw'], 'trailortitle': ['It Follows Official Trailer 1 (2015) - Horror Movie HD']}, {'Title': 'A Quiet Place', 'Year': '2018', 'Rated': 'PG-13', 'Released': '06 Apr 2018', 'Runtime': '90 min', 'Genre': 'Drama, Horror, Sci-Fi', 'Director': 'John Krasinski', 'Writer': 'Bryan Woods, Scott Beck, John Krasinski', 'Actors': 'Emily Blunt, John Krasinski, Millicent Simmonds', 'Plot': 'A family struggles for survival in a world invaded by blind alien creatures with ultra-sensitive hearing.', 'Language': 'American Sign , English', 'Country': 'United States', 'Awards': 'Nominated for 1 Oscar. 38 wins & 129 nominations total', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMjI0MDMzNTQ0M15BMl5BanBnXkFtZTgwMTM5NzM3NDM@._V1_SX300.jpg', 'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'}, {'Source': 'Rotten Tomatoes', 'Value': '96%'}, {'Source': 'Metacritic', 'Value': '82/100'}], 'Metascore': '82', 'imdbRating': '7.5', 'imdbVotes': '616,908', 'imdbID': 'tt6644200', 'Type': 'movie', 'DVD': 'N/A', 'BoxOffice': '$188,024,361', 'Production': 'N/A', 'Website': 'N/A', 'Response': 'True', 'youtubeurl': ['https://www.youtube.com/embed/WR7cc5t7tv8'], 'trailortitle': ['A Quiet Place (2018) - Official Trailer - Paramount Pictures']}, {'Title': 'Get Out', 'Year': '2017', 'Rated': 'R', 'Released': '24 Feb 2017', 'Runtime': '104 min', 'Genre': 'Horror, Mystery, Thriller', 'Director': 'Jordan Peele', 'Writer': 'Jordan Peele', 'Actors': 'Daniel Kaluuya, Allison Williams, Bradley Whitford', 'Plot': "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception of him eventually reaches a boiling point.", 'Language': 'English, Swahili', 'Country': 'United States, Japan', 'Awards': 'Won 1 Oscar. 154 wins & 214 nominations total', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMjUxMDQwNjcyNl5BMl5BanBnXkFtZTgwNzcwMzc0MTI@._V1_SX300.jpg', 'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.8/10'}, {'Source': 'Rotten Tomatoes', 'Value': '98%'}, {'Source': 'Metacritic', 'Value': '85/100'}], 'Metascore': '85', 'imdbRating': '7.8', 'imdbVotes': '740,263', 'imdbID': 'tt5052448', 'Type': 'movie', 'DVD': '09 May 2017', 'BoxOffice': '$176,196,665', 'Production': 'Universal Pictures, QC Entertainment, Blumhouse Productions', 'Website': 'N/A', 'Response': 'True', 'youtubeurl': ['https://www.youtube.com/embed/DzfpyUB60YY'], 'trailortitle': ['Get Out Official Trailer 1 (2017) - Daniel Kaluuya Movie']}, {'Title': 'The Witch', 'Year': '2015', 'Rated': 'R', 'Released': '19 Feb 2016', 'Runtime': '92 min', 'Genre': 'Drama, Fantasy, Horror', 'Director': 'Robert Eggers', 'Writer': 'Robert Eggers', 'Actors': 'Anya Taylor-Joy, Ralph Ineson, Kate Dickie', 'Plot': 'An isolated Puritan family in 1630s New England comes unraveled by the forces of witchcraft and possession.', 'Language': 'English', 'Country': 'United States, Canada, United Kingdom', 'Awards': '43 wins & 72 nominations total', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMTUyNzkwMzAxOF5BMl5BanBnXkFtZTgwMzc1OTk1NjE@._V1_SX300.jpg', 'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.0/10'}, {'Source': 'Rotten Tomatoes', 'Value': '91%'}, {'Source': 'Metacritic', 'Value': '84/100'}], 'Metascore': '84', 'imdbRating': '7.0', 'imdbVotes': '321,234', 'imdbID': 'tt4263482', 'Type': 'movie', 'DVD': 'N/A', 'BoxOffice': '$25,138,705', 'Production': 'N/A', 'Website': 'N/A', 'Response': 'True', 'youtubeurl': ['https://www.youtube.com/embed/iQXmlf3Sefg'], 'trailortitle': ['The Witch | Official Trailer HD | A24']}, {'Title': 'Sinister', 'Year': '2012', 'Rated': 'R', 'Released': '12 Oct 2012', 'Runtime': '110 min', 'Genre': 'Horror, Mystery, Thriller', 'Director': 'Scott Derrickson', 'Writer': 'Scott Derrickson, C. Robert Cargill', 'Actors': 'Ethan Hawke, Juliet Rylance, James Ransone', 'Plot': 'A controversial true-crime writer finds a box of Super 8 home movies in his new home, revealing that the murder case he is currently researching could be the work of an unknown serial killer whose legacy dates back to the 1960s.', 'Language': 'English', 'Country': 'United States, United Kingdom, Canada', 'Awards': '3 wins & 14 nominations', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMjI5MTg1Njg0Ml5BMl5BanBnXkFtZTcwNzg2Mjc4Nw@@._V1_SX300.jpg', 'Ratings': [{'Source': 'Internet Movie Database', 'Value': '6.8/10'}, {'Source': 'Rotten Tomatoes', 'Value': '63%'}, {'Source': 'Metacritic', 'Value': '53/100'}], 'Metascore': '53', 'imdbRating': '6.8', 'imdbVotes': '292,589', 'imdbID': 'tt1922777', 'Type': 'movie', 'DVD': 'N/A', 'BoxOffice': '$48,086,903', 'Production': 'N/A', 'Website': 'N/A', 'Response': 'True', 'youtubeurl': ['https://www.youtube.com/embed/_kbQAJR9YWQ'], 'trailortitle': ['Sinister Official Trailer #1 (2012) - Ethan Hawke Horror Movie HD']}, {'Title': 'Us', 'Year': '2019', 'Rated': 'R', 'Released': '22 Mar 2019', 'Runtime': '116 min', 'Genre': 'Horror, Mystery, Thriller', 'Director': 'Jordan Peele', 'Writer': 'Jordan Peele', 'Actors': "Lupita Nyong'o, Winston Duke, Elisabeth Moss", 'Plot': "In order to get away from their busy lives, the Wilson family takes a vacation to Santa Cruz, California. At night, four strangers break into Adelaide's childhood home. The family is shocked to find out that the intruders look lik...", 'Language': 'English', 'Country': 'United States, China, Japan', 'Awards': '86 wins & 134 nominations total', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMzhkMjFkN2YtODU2Ni00YWYwLWExN2MtOWNjZmQxM2U4YTM5XkEyXkFqcGc@._V1_SX300.jpg', 'Ratings': [{'Source': 'Internet Movie Database', 'Value': '6.8/10'}, {'Source': 'Rotten Tomatoes', 'Value': '93%'}, {'Source': 'Metacritic', 'Value': '81/100'}], 'Metascore': '81', 'imdbRating': '6.8', 'imdbVotes': '357,851', 'imdbID': 'tt6857112', 'Type': 'movie', 'DVD': 'N/A', 'BoxOffice': '$175,084,580', 'Production': 'N/A', 'Website': 'N/A', 'Response': 'True', 'youtubeurl': ['https://www.youtube.com/embed/hNCmb-4oXJA'], 'trailortitle': ['Us - Official Trailer [HD]']}, {'Title': 'The Babadook', 'Year': '2014', 'Rated': 'Not Rated', 'Released': '28 Nov 2014', 'Runtime': '94 min', 'Genre': 'Drama, Horror, Mystery', 'Director': 'Jennifer Kent', 'Writer': 'Jennifer Kent', 'Actors': 'Essie Davis, Noah Wiseman, Daniel Henshall', 'Plot': 'A single mother and her child fall into a deep well of paranoia when an eerie children\'s book titled "Mister Babadook" manifests in their home.', 'Language': 'English', 'Country': 'Australia, Canada', 'Awards': '56 wins & 64 nominations total', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMTk0NzMzODc2NF5BMl5BanBnXkFtZTgwOTYzNTM1MzE@._V1_SX300.jpg', 'Ratings': [{'Source': 'Internet Movie Database', 'Value': '6.8/10'}, {'Source': 'Rotten Tomatoes', 'Value': '98%'}, {'Source': 'Metacritic', 'Value': '86/100'}], 'Metascore': '86', 'imdbRating': '6.8', 'imdbVotes': '257,639', 'imdbID': 'tt2321549', 'Type': 'movie', 'DVD': 'N/A', 'BoxOffice': '$964,413', 'Production': 'N/A', 'Website': 'N/A', 'Response': 'True', 'youtubeurl': ['https://www.youtube.com/embed/k5WQZzDRVtw'], 'trailortitle': ['The Babadook Official Trailer #1 (2014) - Essie Davis Horror Movie HD']}, {'Response': 'False', 'Error': 'Movie not found!', 'youtubeurl': ['https://www.youtube.com/embed/3eqxXqJDmcY'], 'trailortitle': ['THE HAUNTING OF HILL HOUSE Official Trailer (2018) Netflix, Horror Movie']}, {'Title': 'The Invisible Man', 'Year': '2020', 'Rated': 'R', 'Released': '28 Feb 2020', 'Runtime': '124 min', 'Genre': 'Drama, Horror, Mystery', 'Director': 'Leigh Whannell', 'Writer': 'Leigh Whannell, H.G. Wells', 'Actors': 'Elisabeth Moss, Oliver Jackson-Cohen, Harriet Dyer', 'Plot': "When Cecilia's abusive ex takes his own life and leaves her his fortune, she suspects his death was a hoax. As a series of coincidences turn lethal, Cecilia works to prove that she is being hunted by someone nobody can see.", 'Language': 'English', 'Country': 'Australia, United States', 'Awards': '43 wins & 84 nominations', 'Poster': 'https://m.media-amazon.com/images/M/MV5BYTM3NDJhZWUtZWM1Yy00ODk4LThjNmMtNDg3OGYzMGM2OGYzXkEyXkFqcGc@._V1_SX300.jpg', 'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.1/10'}, {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72', 'imdbRating': '7.1', 'imdbVotes': '264,896', 'imdbID': 'tt1051906', 'Type': 'movie', 'DVD': 'N/A', 'BoxOffice': '$70,410,000', 'Production': 'N/A', 'Website': 'N/A', 'Response': 'True', 'youtubeurl': ['https://www.youtube.com/embed/WO_FJdiY9dA'], 'trailortitle': ['The Invisible Man - Official Trailer [HD]']}, {'Title': 'Train to Busan', 'Year': '2016', 'Rated': 'Not Rated', 'Released': '20 Jul 2016', 'Runtime': '118 min', 'Genre': 'Action, Horror, Thriller', 'Director': 'Yeon Sang-ho', 'Writer': 'Park Joo-suk, Yeon Sang-ho', 'Actors': 'Gong Yoo, Jung Yu-mi, Ma Dong-seok', 'Plot': 'While a zombie virus breaks out in South Korea, passengers struggle to survive on the train from Seoul to Busan.', 'Language': 'Korean, Hawaiian, English', 'Country': 'South Korea', 'Awards': '36 wins & 42 nominations total', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMTkwOTQ4OTg0OV5BMl5BanBnXkFtZTgwMzQyOTM0OTE@._V1_SX300.jpg', 'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.6/10'}, {'Source': 'Rotten Tomatoes', 'Value': '95%'}, {'Source': 'Metacritic', 'Value': '73/100'}], 'Metascore': '73', 'imdbRating': '7.6', 'imdbVotes': '273,591', 'imdbID': 'tt5700672', 'Type': 'movie', 'DVD': 'N/A', 'BoxOffice': '$2,129,768', 'Production': 'N/A', 'Website': 'N/A', 'Response': 'True', 'youtubeurl': ['https://www.youtube.com/embed/1ovgxN2VWNc'], 'trailortitle': ['Train to Busan Official Trailer 1 (2016) - Yoo Gong Movie']}, {'Title': 'The Cabin in the Woods', 'Year': '2011', 'Rated': 'R', 'Released': '13 Apr 2012', 'Runtime': '95 min', 'Genre': 'Horror, Mystery, Thriller', 'Director': 'Drew Goddard', 'Writer': 'Joss Whedon, Drew Goddard', 'Actors': 'Kristen Connolly, Chris Hemsworth, Anna Hutchison', 'Plot': 'A group of kids go to a remote cabin in the woods where their fate is unknowingly controlled by technicians as part of a world-wide conspiracy where all horror movie clichés are revealed to be part of an elaborate sacrifice ritual.', 'Language': 'English, Japanese', 'Country': 'Canada, United States', 'Awards': '20 wins & 34 nominations', 'Poster': 'https://m.media-amazon.com/images/M/MV5BNTUxNzYyMjg2N15BMl5BanBnXkFtZTcwMTExNzExNw@@._V1_SX300.jpg', 'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.0/10'}, {'Source': 'Rotten Tomatoes', 'Value': '92%'}, {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72', 'imdbRating': '7.0', 'imdbVotes': '463,684', 'imdbID': 'tt1259521', 'Type': 'movie', 'DVD': 'N/A', 'BoxOffice': '$42,073,277', 'Production': 'N/A', 'Website': 'N/A', 'Response': 'True', 'youtubeurl': ['https://www.youtube.com/embed/NsIilFNNmkY'], 'trailortitle': ['Cabin in the Woods (2012 Movie) - Official Trailer - Chris Hemsworth &amp; Jesse Williams']}, {'Response': 'False', 'Error': 'Movie not found!', 'youtubeurl': ['https://www.youtube.com/embed/xKJmEC5ieOk'], 'trailortitle': ['IT - Official Trailer 1']}]
def index(request):
    return render(request, 'chat/index.html')

def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        print(confirmation)
        if password != confirmation:
            return render(request, 'chat/signup.html', {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'chat/signup.html', {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("chat:home"))
    else:
        return render(request, 'chat/signup.html',{"show_main":True})
   
   

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("chat:home"))
        else:
            return render(request, "chat/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "chat/login.html",
                      {"show_main":True})



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))

def home(request):
    
    if request.user.is_authenticated:
        if request.method == "POST":
            # mood = request.POST["mood"]
            # genre = request.POST["genre"]
            # reason = request.POST["reason"]
            # emotion = request.POST["emotion"]
            # return render(request, 'chat/home.html')
            # mood = "angry"
            # genre = "horror"
            # reason = "it is cold"
            # emotion = "thrilling"
            # movie_names = []
            # gpt_api = settings.SECRET_KEY
            # ombl_api_key = settings.API_KEY
            # current_content = ""
            # asking = "Can you generation movies list? I am feeling " + mood + " and I want to watch " + genre + " because " + reason + " and I am " + emotion +"Give me only movie name list"
            # client = OpenAI(api_key=gpt_api)


            # stream = client.chat.completions.create(
            # model="gpt-4o-mini",
            # messages=[{"role": "user", "content": asking}],
            # stream=True,
            # )
            # print(stream)
            # for part in stream:
            #     content =part.choices[0].delta.content or ""
            #     current_content += content
            # lst = [line.strip() for line in current_content.split("\n") if line.strip()] 
            # for i in lst:
            #     if i[0].isdigit():
            #         movie_names.append(i.split(".")[1].strip())
            # search_movies(movie_names)
            # print(movies_detail)
            
    
            

            return render(request, 'chat/display.html',{
                "movies":movies_detail,
                'show_main': False,
            })
        else:
            return render(request, 'chat/home.html',{
        "show_main":True
    })
    else:
        return HttpResponseRedirect(reverse("chat:login"))
    

def apirequest(request, movie_name):
    if request.method == "GET":
        mydict = ""
        for i in movies_detail:  # Assuming `movies_detail` is a list of movie dictionaries
            if 'Title' in i and i['Title'] == movie_name:
                mydict = i
                break
        
        if mydict:  # If a matching movie is found
            return JsonResponse(mydict, safe=False)  # Directly return the dictionary
        else:  # If no matching movie is found
            return JsonResponse({"error": "Movie not found"}, status=404)

def display(request):
    return render(request, 'chat/display.html',{
                "movies":movies_detail,
                'show_main': False,
            })


def search_movies(movies):
    
    youtube_API_key = settings.YOUTUBE_API 
    print(youtube_API_key)
    OMDB_API_key = settings.API_KEY
    for i in movies:
        mydict ={}
        url = f"http://www.omdbapi.com/?t={i}&apikey={OMDB_API_key}"
        youtubeurl = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={i}+trailer&type=video&maxResults=1&key={youtube_API_key}"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            mydict =data
            
            
        print(requests.get(youtubeurl))
        youtubereponse = requests.get(youtubeurl)
        if youtubereponse.status_code == 200:
            data = youtubereponse.json()
            hein = []
            titles =[]
            items = data.get('items', [])
            for i in items:
            # Ensure 'id' and 'videoId' exist in the item
                if 'snippet' in i  and 'title' in i['snippet']:
                    titles.append(i['snippet']['title'])
                if 'id' in i and 'videoId' in i['id']:
                    hein.append(f"https://www.youtube.com/embed/{i['id']['videoId']}")
            mydict["youtubeurl"] =hein
            mydict["trailortitle"] = titles
            print(hein)
        movies_detail.append(mydict)

def watchlist(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)