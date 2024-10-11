from django import forms
from django.contrib.auth.models import User
from . models import Review,Favorite,Reservation
"""
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
"""
class UserProfileForm(forms.ModelForm):
    # パスワードフィールドをオプションにするが、フォーム送信時に空ならエラーメッセージを表示する
    password = forms.CharField(
        required=False,  # 必須ではない
        widget=forms.PasswordInput(attrs={'placeholder': '新しいパスワードを入力してください'}),
        help_text='8文字以上、大文字・小文字・数字を含む必要があります。',
        min_length=8
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']  # 必要なフィールドを指定

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        # 必須フィールドが空の場合、エラーメッセージを追加
        if not email:
            self.add_error('email', 'メールアドレスは必須です。')
        if not first_name:
            self.add_error('first_name', '名前は必須です。')
        if not last_name:
            self.add_error('last_name', '苗字は必須です。')

        # もしパスワードが入力されている場合、そのバリデーション
        password = cleaned_data.get('password')
        if password and len(password) < 8:
            self.add_error('password', 'パスワードは8文字以上である必要があります。')

        return cleaned_data

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