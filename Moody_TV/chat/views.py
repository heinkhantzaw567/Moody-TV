from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import User
from django.db import IntegrityError
from openai import OpenAI
import requests
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Movie
movies_detail =[]
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
    return HttpResponseRedirect(reverse("chat:index"))

def home(request):
    
    if request.user.is_authenticated:
        if request.method == "POST":
            mood = request.POST["mood"]
            genre = request.POST["genre"]
            reason = request.POST["reason"]
            
            # return render(request, 'chat/home.html')
            
            movie_names = []
            gpt_api = settings.SECRET_KEY
            ombl_api_key = settings.API_KEY
            current_content = ""
            asking = "Can you generation movies list? I am feeling " + mood + " and I want to watch " + genre + " because " + reason +"Give me only movie name list"
            client = OpenAI(api_key=gpt_api)


            stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": asking}],
            stream=True,
            )
            print(stream)
            for part in stream:
                content =part.choices[0].delta.content or ""
                current_content += content
            lst = [line.strip() for line in current_content.split("\n") if line.strip()] 
            for i in lst:
                if i[0].isdigit():
                    movie_names.append(i.split(".")[1].strip())
            search_movies(movie_names)
            print(movies_detail)
            
    
            

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
    
@csrf_exempt
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
        youtubereponse = requests.get(youtubeurl)
        if response.status_code == 200 and youtubereponse.status_code == 200:
            data = response.json()
            mydict =data
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

@csrf_exempt
def watchlist(request):
    if request.method == "POST":

        data = json.loads(request.body)
        print(data["Title"])
        print(request.user)
        # Create a new Movie object
        movie = Movie(
            userid= request.user,
            title=data["Title"],
            released=data["Released"],
            rated=data["Rated"],
            runtime=data["Runtime"],
            Genre=data["Genre"],  # Corrected to lowercase 'genre'
            Director=data["Director"],
            Actors=data["Actors"],
            trailer=data["youtubeurl"],
            plot=data["Plot"],
            poster=data["Poster"]
        )

        # Save the movie object to the database
        movie.save()

        # Return a success response
        return JsonResponse({"message": "Movie record created successfully!"}, safe=False)
    else:
        watchlist = Movie.objects.filter(userid=request.user)
        return render(request,'chat/watchlist.html',{
            'show_main': False,
            "watchlist": watchlist
        })
    
@csrf_exempt
@login_required
def watchlistdatabase(request,movie_name):
    if request.method == "GET":
        watchlist = Movie.objects.filter(userid=request.user, title=movie_name)

        if not watchlist.exists():
            return JsonResponse({"error": "Movie not found in watchlist"}, status=404)

        # Convert queryset to a list of dictionaries
        data =  list(watchlist.values())  

        return JsonResponse(data, safe=False)

    elif request.method == "DELETE":
        try:
            watchlist = Movie.objects.filter(userid=request.user, title=movie_name)

            if not watchlist.exists():
                return JsonResponse({"error": "Movie not found in watchlist"}, status=404)

            watchlist.delete()
            return JsonResponse({"message": "Movie record deleted successfully!"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


     