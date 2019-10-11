from django import forms

class YouTubeForm(forms.Form):
    video = forms.FileField()
    title = forms.CharField(max_length=30)
    description = forms.CharField(max_length=30)


class BlockChainSignUpForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=30)
    mobile = forms.CharField(max_length=30)
    blockchain_account_name = forms.CharField(max_length=30)
    
