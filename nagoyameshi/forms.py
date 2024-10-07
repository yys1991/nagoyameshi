from django import forms
from django.contrib.auth.models import User
from . models import Review,Favorite,Reservation

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="新しいパスワード")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            return None  # パスワードが空の場合は変更しない
        return password


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = [ "restaurant","user","content" ]



class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ["restaurant","user"]


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [ "restaurant","user","datetime","headcount" ]