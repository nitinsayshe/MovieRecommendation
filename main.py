import requests
from flask import Flask,render_template,request
import pickle
import pandas as pd


movies_list=pickle.load(open('movies.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
movies=movies_list
#print(movies['title'].values)

app =Flask(__name__,template_folder='template')
context = movies['title'].values


import requests
def get_url(movieid):
    response=requests.get("https://api.themoviedb.org/3/movie/{movieid}?api_key=aa40366f6803c5373a43b45e749eefa0&language=en-US".format(movieid=movieid))
    data=response.json()
    return "http://image.tmdb.org/t/p/w500"+data['poster_path']

@app.route("/" , methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        select = request.form.get('comp_select')
        movie_index = movies[movies['title'] == str(select)].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:9]
        recommended_movies = []
        recommended_movies_poster=[]
        for i in movie_list:
            print("id",i[0])
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_poster.append((get_url(movies.iloc[i[0]].movie_id)))
        print(recommended_movies)
        print(recommended_movies_poster)
        recommendation=dict(zip(recommended_movies, recommended_movies_poster))
        print(recommendation)
        return render_template('home.html',recommendation=recommendation,context=context)
    else:

        return render_template('home.html', context=context)



if __name__== "__main__":
    app.run(debug=True)