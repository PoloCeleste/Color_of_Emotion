import requests
import json
from pprint import pprint

results=[]
TMDB='API_TOKEN'
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB}"
}

popular_url = "https://api.themoviedb.org/3/discover/movie"
poster_url = "https://image.tmdb.org/t/p/original"
de=['adult', 'backdrop_path', 'video', 'popularity', 'vote_count']
set_provider=(8,119,337,356,97,350)

for i in range(1, 51):
    movie_params = {
        'sort_by':'popularity.desc',
        'include_adult':False,
        'include_video':False,
        'language':'ko-KR',
        'page':1,
        'vote_average.gte':6,
        'vote_count.gte':150,
        'watch_region':'KR',
        'with_watch_providers':'8|119|337|356|97|350',
        #Netflix | Amazon Prime Video | Disney Plus | wavve | Watcha | Apple TV Plus
        # 'with_watch_monetization_types':'flatrate|free|ads',
    }

    responses = requests.get(popular_url, headers=headers, params=movie_params).json()['results']

    for response in responses:
        for d in de:
            del response[d]
        
        response['poster_path'] = poster_url+response['poster_path']
        
        tmdb_vote_average=response['vote_average']
        del response['vote_average']
        response['tmdb_vote_average']=tmdb_vote_average
        
        movie_id = response['id']
        providers_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"
        providers = requests.get(providers_url, headers=headers).json()['results']['KR']
        p=set()
        for key, value in providers.items():
            if key=='link':continue
            for v in value:
                pid=v['provider_id']
                if pid in set_provider: p.add(pid)
        if p: response['watch_providers']=list(p)

    results+=responses




with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)
print(len(results))
