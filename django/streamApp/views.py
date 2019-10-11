from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.views.generic.base import View

# from oauth2client.client import flow_from_clientsecrets, OAuth2WebServerFlow
# from oauth2client.contrib import xsrfutil
# from oauth2client.contrib.django_util.storage import DjangoORMStorage
# from .models import CredentialsModel


import tempfile
from django.http import HttpResponse, HttpResponseBadRequest
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from .models import BlockChainModel
import requests
import json
from .forms import YouTubeForm, BlockChainSignUpForm
# Create your views here.


# flow = OAuth2WebServerFlow(
#     client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
#     client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
#     scope='https://www.googleapis.com/auth/youtube',
#     redirect_uri='http://127.0.0.1:8000/oauth2callback/')

def index(request):
    url = 'https://dry-brushlands-44237.herokuapp.com/ss'
    r = requests.get(url)
    print("url: ",r.text)
    return render(request, "index.html")

def trending(request):
    return render(request, "trending.html")

def passbook(request):
    return render(request, "passbook.html")


class Videocreate(FormView):
    template_name = "videocreate.html"
    form_class = YouTubeForm

    def form_valid(self, form):
        fname = form.cleaned_data['video'].temporary_file_path()
        video_title = form.cleaned_data['title']
        video_desc = form.cleaned_data['description']
        storage = DjangoORMStorage(
            CredentialsModel, 'id', self.request.user.id, 'credential')
        credentials = storage.get()

        client = build('youtube', 'v3', credentials=credentials)

        body = {
            'snippet': {
                'title': video_title,        #'My Django Youtube Video',
                'description': video_desc,    #'My Django Youtube Video Description',
                'tags': 'django,howto,video,api',
                'categoryId': '27'
            },
            'status': {
                'privacyStatus': 'public'
            }
        }

        with tempfile.NamedTemporaryFile('wb', suffix='yt-django') as tmpfile:
            with open(fname, 'rb') as fileobj:
                tmpfile.write(fileobj.read())
                insert_request = client.videos().insert(
                    part=','.join(body.keys()),
                    body=body,
                    media_body=MediaFileUpload(
                        tmpfile.name, chunksize=-1, resumable=True)
                )
                insert_request.execute()

        return redirect('/')



class AuthorizeView(View):

    def get(self, request, *args, **kwargs):
        storage = DjangoORMStorage(
            CredentialsModel, 'id', request.user.id, 'credential')
        credential = storage.get()
        flow = OAuth2WebServerFlow(
            client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
            client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            scope='https://www.googleapis.com/auth/youtube',
            redirect_uri='http://127.0.0.1:8000/oauth2callback/')
        if credential is None or credential.invalid == True:
            flow.params['state'] = xsrfutil.generate_token(
                settings.SECRET_KEY, request.user)
            authorize_url = flow.step1_get_authorize_url()

            return redirect(authorize_url)
        print("credential :",credential)      #credential for sign in youtube user

        return redirect('blockchainsignup')


# class Oauth2CallbackView(View):

#     def get(self, request, *args, **kwargs):
#         if not xsrfutil.validate_token(
#             settings.SECRET_KEY, request.GET.get('state').encode(),
#             request.user):
#                 return HttpResponseBadRequest()
#         credential = flow.step2_exchange(request.GET)
#         storage = DjangoORMStorage(
#             CredentialsModel, 'id', request.user.id, 'credential')
#         storage.put(credential)

#         return redirect('/videocreate/')

#         def get(self, request, *args, **kwargs):
#             storage = DjangoORMStorage(
#                 CredentialsModel, 'id', request.user.id, 'credential')
#             credential = storage.get()

#             if credential is None or credential.invalid == True:
#                 flow.params['state'] = xsrfutil.generate_token(
#                     settings.SECRET_KEY, request.user)
#                 authorize_url = flow.step1_get_authorize_url()
#                 return redirect(authorize_url)
#             return redirect('/videocreate/')


class BlockChainSignUp(View):

    def get(self, request, *args, **kwargs):
        return render(request,'blockchainsignup.html',{'form':BlockChainSignUpForm})
    def post(self, request, *args, **kwargs):
        p = BlockChainModel(name = request.POST['name'],email= request.POST['email'],mobile= request.POST['mobile'],blockchain_account_name= request.POST['blockchain_account_name'])
        p.save()
        # BlockChainModel.name = request.POST["name"
        # BlockChainModel.save()


        print(request.POST["name"])
        return redirect('/')


def myvideo(request):
    return render(request, 'myvideo.html')


def hotofferings(request):
    return render(request, 'hotofferings.html')
