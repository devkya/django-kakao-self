from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from kakao_login_self.settings import SOCIAL_OUTH_CONFIG
from rest_framework.decorators import api_view, permission_classes
import requests
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

BASE_URL = "http://localhost:8000/"
KAKAO_CALLBACK_URI = BASE_URL + 'accounts/kakao/login/callback/'

def index(request):
    # FK가 검색 필드에 포함되어 일어나는 error
    # 해결 : 참조하고 있는 클래스에 instance 
    return render(request, 'index.html')

class KakaoSignIncallBackView(View):
    def get(self, request):
        auth_code = request.GET.get('code')
        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        data = {
            'grant_type': 'authorization_code',
            'client_id': SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY'],
            'redirect_url': SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI'],
            'client_secret': SOCIAL_OUTH_CONFIG['KAKAO_SECRET_KEY'],
            'code': auth_code
        }
        
        token_response = requests.post(kakao_token_api, data=data)
        access_token = token_response.json()
        print(access_token)
        user_info_response = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer ${access_token}"})
        return JsonResponse({'user_info' : user_info_response.json()})
        
        
# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny, ])
def kakao_login(request):
    CLIENT_ID = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
    REDIRECT_URL = SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI']
    url = "https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={0}&redirect_uri={1}".format(
    CLIENT_ID, REDIRECT_URL)
    res = redirect(url)
    return res

@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_user_info(request):
    # CODE = request.query_params['code']
    CODE = request.GET.get('code')
    url = "https://kauth.kakao.com/oauth/token"
    res = {
    'grant_type': 'authorization_code',
    'client_id': SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY'],
    'redirect_url': SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI'],
    'client_secret': SOCIAL_OUTH_CONFIG['KAKAO_SECRET_KEY'],
    'code': CODE
    }
    headers = {
    'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    response = requests.post(url, data=res, headers=headers)
    token_json = response.json()
    user_url = "https://kapi.kakao.com/v2/user/me"
    auth = "Bearer " + token_json['access_token']
    HEADER = {
        "Authorization": auth,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    res = requests.get(user_url, headers=HEADER)
    print(response.json())
    return Response(res.text)
