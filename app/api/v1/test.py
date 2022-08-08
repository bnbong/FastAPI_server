# TODO: make token refresh function's testcase.

# following spotify code flow from https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
from ...test_session_maker import *
import uuid

def test_make_16_bytes_uuid():
    uuid_str = uuid.uuid4().bytes
    
    assert not None == uuid_str
    assert 16 == len(uuid_str)

def test_could_make_string_into_url_format():
    import urllib

    client_id = 'the_client_id'
    redirect_uri = 'https://testhost.com/callback/'
    state = 'spotify_state'

    request_data = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': 'user-read-email',
        'redirect_uri': redirect_uri,
        'state': state
    }
    test_authorize_uri = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(request_data)
    
    assert "https://accounts.spotify.com/authorize?response_type=code&client_id=the_client_id&scope=user-read-email&redirect_uri=https%3A%2F%2Ftesthost.com%2Fcallback%2F&state=spotify_state"\
        == test_authorize_uri

def test_could_authorize_spotify():
    """
    request data:
        cliend_id, response_type, redirect_url, state, scope

    response data:
        code, state
    """
    response = client.get('/api/v1/spotify/login')

    assert 200 == response.status_code

def test_could_get_account_json_response_from_spotify():
    """
    request data:
        access_token

    response data:
        {JSON object}
    """
    from dotenv import load_dotenv

    import os
    import base64

    load_dotenv()

    code = 'default_code'
    state = 'spotify_state'
    response = client.get('/api/v1/spotify/callback?code={code}&state={state}')

    assert 200 == response.status_code

def test_could_get_refreshed_access_token_from_spotify():
    """
    request data:
        access_token

    response data:
        {JSON object}
    """
    response = client.get('/api/v1/spotify/refresh_token')

    assert 200 == response.status_code
