from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
import base64
import requests


client_key = 'ljkFvgv4WCo7M0CD2XTgEwlhs'  # your key
client_secret = 'kkkAp297einH366PUrZPxUqZDLNjKvqJShDmzKilA2492jvLQ2'  # your secret key
bearer_token = 'Bearer AAAAAAAAAAAAAAAAAAAAAAHQUQEAAAAA8SZ6L4UMIFxrjnml5%2FFSOXzAW%2Fc%3DH5jrh90TvkyoAotjjUhiMlETpezRSofSKwZScmQJfBzQnHQm8C'  # your token
base_url = 'https://api.twitter.com/'
search_url = base_url+'1.1/search/tweets.json'
status_code = 'status_code'


def home(request):
    return render(request, 'home.html')


def search_twt(request):
    # encode your keys
    key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
    # use base64 to encode the keys to binary
    b64_encoded_key = base64.b64encode(key_secret)
    # convert to ascii
    b64_encoded_key = b64_encoded_key.decode('ascii')
    auth_endpoint = base_url+'oauth2/token'
    auth_headers = {'Authorization': 'Basic {}'.format(b64_encoded_key),
                    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    auth_data = {'grant_type': 'client_credentials'}
    # Post Request
    response = requests.post(
        auth_endpoint, headers=auth_headers, data=auth_data)
    json_data = response.json()
    '''
    {'token_type': 'bearer',
    'access_token': 'your token will be here'}
    '''
    access_token = json_data['access_token']
    search_headers = {'Authorization': bearer_token.format(access_token)
                      }

    if request.method == "POST":
        searched = request.POST['searched']
        if searched == '':
            return render(request, 'ifnot_searched.html')
        cryptop = request.POST.getlist('cryptop', False)
        twtcount = request.POST.get('twtcount', False)
        if twtcount == '':
            return render(request, 'ifnot_count.html')
        filter = request.POST['filter']
        search = ''
        if cryptop == False:
            search = searched
        else:
            for crypto in cryptop:
                search = search + '+' + crypto

        parameters = {'q': searched + search,
                      'result_type': filter,
                      'count': twtcount}

        response = requests.get(
            search_url, headers=search_headers, params=parameters)
        tweet = response.json()

        return render(request, 'home.html', {'searched': searched, 'data': tweet['statuses']})

    else:
        return render(request, 'home.html')
