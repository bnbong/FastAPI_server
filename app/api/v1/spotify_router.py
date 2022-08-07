from fastapi import APIRouter, Header
from fastapi.responses import RedirectResponse

from enum import Enum
from typing import Optional, Union

from dotenv import load_dotenv

import os
import requests
import urllib

load_dotenv()

router = APIRouter()


@router.get('/spotify/login/', status_code=200)
def get_spotify_login():
    url = 'https://accounts.spotify.com/authorize'
    scope = 'user-read-private user-read-email'

    request_data = {
        'response_type': 'code',
        'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
        'scope': scope,
        'redirect_uri': os.getenv('SPOTIFY_REDIRECT_URI'),
        'state': os.getenv('SPOTIFY_STATE'),
    }
    spotify_authorize_uri = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(request_data)
    # response = requests.get(spotify_authorize_uri)
    return RedirectResponse(url=spotify_authorize_uri)

@router.get('/spotify/callback/')
async def get_token_from_spotify(Authorization: Union[str, None] = Header(default=None), \
    Content_Type: Union[str, None] = Header(default='application/x-www-form-urlencoded', convert_underscores=False) ,\
    state: str = None, code: str = None):

    if state == None:
        return {'error': 'state_mismatch'}
    else:
        url = 'https://accounts.spotify.com/api/token'
        request_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': os.getenv('SPOTIFY_REDIRECT_URI'),
            "client_id": os.getenv('SPOTIFY_CLIENT_ID'),
            "client_secret": os.getenv('SPOTIFY_CLIENT_SECRET')
        }
        response = requests.post(url, data=request_data)

        return response.json()

@router.get('/spotify/refresh_token/')
async def get_refresh_token_from_spotify(Authorization: Union[str, None] = Header(default=None), \
    Content_Type: Union[str, None] = Header(default='application/x-www-form-urlencoded', convert_underscores=False) ,\
    refresh_token: str = None):
    
    url = 'https://accounts.spotify.com/api/token'
    request_data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        "client_id": os.getenv('SPOTIFY_CLIENT_ID'),
        "client_secret": os.getenv('SPOTIFY_CLIENT_SECRET')
    }
    response =  requests.post(url, data=request_data)

    return response.json()
