from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
from .models import Restaurant,Category,Review,Favorite,Reservation,PremiumUser
from .forms import ReviewForm,FavoriteForm,ReservationForm
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin

from django.conf import settings
from django.urls import reverse_lazy
import stripe
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


stripe.api_key  = settings.STRIPE_API_KEY



# TODO:修正1
# https://noauto-nolife.com/post/django-http-response/
from django.http import HttpResponseForbidden


# TODO:修正2 
# メール認証(検証)をしていない場合は、メール確認ページへリダイレクトさせる。
# LoginRequiredMixinをオーバーライドする。
# 参照: https://noauto-nolife.com/post/django-create-origin-mixin/

from allauth.account.admin import EmailAddress
from django.contrib.auth.mixins import AccessMixin
"""
class LoginRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not EmailAddress.objects.filter(user=request.user.id,verified=True).exists():
            print("メールの確認が済んでいません")
            return redirect("account_email")

        #HttpResponseを返却する。
        return super().dispatch(request, *args, **kwargs)

"""




class CancelReservationView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # ログインユーザーが予約したものかを確認
        reservation = get_object_or_404(Reservation, id=pk, user=request.user)

        # 予約が見つかったら削除
        reservation.delete()

        # 予約が削除された後、マイページにリダイレクト
        return redirect("mypage")

class TopView(View):
    def get(self,request):
        query = Q()

        if"search" in request.GET:
           print(request.GET["search"])


           words = request.GET["search"].replace("　"," ").split(" ")
           print(words)


           for word in words:
               query &= Q(name__icontains=word)


        if "category" in request.GET:
            print( request.GET["category"] )       
            if "" != request.GET["category"]:
                query &= Q(category=request.GET["category"])


        restaurants = Restaurant.objects.filter(query)

        categories = Category.objects.all()

        context={
            "restaurants":restaurants,
            "greet":"こんにちは",
            "price":1000,
            "categories":categories
        }

        return render(request,"top.html",context)



"""class RestaurantView(LoginRequiredMixin,View):
    def get(self,request,pk):
        
        print(pk)

        context = {}

        context["restaurant"] = Restaurant.objects.filter(id=pk).first()

        context["reviews"] = Review.objects.filter(restaurant=pk)

        return render(request, "restaurant.html",context)
"""
class RestaurantView(LoginRequiredMixin, View):
    def get(self, request, pk):
        restaurant = Restaurant.objects.filter(id=pk).first()

        # 現在のレストランがユーザーのお気に入りに登録されているかチェック
        is_favorite = Favorite.objects.filter(user=request.user, restaurant=restaurant).exists()

        context = {
            "restaurant": restaurant,
            "reviews": Review.objects.filter(restaurant=pk),
            "is_favorite": is_favorite,  # お気に入りかどうかのフラグをコンテキストに追加
        }

        return render(request, "restaurant.html", context)


"""class ReviewView(LoginRequiredMixin, View):
    def post(self,request,pk):

        print(pk, "に対してレビュー")

        restaurant = Restaurant.objects.filter(id=pk).first()
        request.user
        request.POST["content"]        

        
        review = Review(restaurant=restaurant, user=request.user, content=request.POST["content"])
        review.save()   
        
        
        copied = request.POST.copy()
        copied["user"] = request.user
        copied["restaurant"] = restaurant

        ReviewForm(copied)    

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print(form.errors)

        return redirect("top")
"""
class ReviewView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print(pk, "に対してレビュー")

        # レストランを取得
        restaurant = Restaurant.objects.filter(id=pk).first()

        # 1. ユーザーが有料会員かどうかを確認
        if not PremiumUser.objects.filter(user=request.user).exists():
            # 無料会員の場合、エラーメッセージを渡してレストラン詳細ページに戻る
            return render(request, "restaurant.html", {
                "restaurant": restaurant,
                "error": "有料会員のみレビューを投稿できます。"  # ここでエラーメッセージを渡す
            })

        # POSTデータのコピー
        form = ReviewForm(request.POST)

        # userとrestaurantをフォームのインスタンスにセット
        form.instance.user = request.user
        form.instance.restaurant = restaurant

        if form.is_valid():  # バリデーションチェック
            print("バリデーションOK")
            form.save()  # フォームデータを保存
            return redirect("restaurant", pk=pk)  # レストラン詳細ページにリダイレクト
        else:
            print(form.errors)  # バリデーションエラーがあれば表示
            # フォームが無効な場合、エラーとともにレストラン詳細ページにリダイレクト
            return render(request, "restaurant.html", {
                "restaurant": restaurant,
                "form": form,  # フォームのエラーも渡す
                "error": "レビューの投稿に失敗しました。"  # 失敗時のエラーメッセージ
            })


"""class FavoriteView(LoginRequiredMixin,View):
    def post(self, request,pk):
        restaurant = Restaurant.objects.filter(id=pk).first()

        copied = request.POST.copy()
        copied["user"] = request.user
        copied["restaurant"] = restaurant

        form = FavoriteForm(copied)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print(form.errors)

        return redirect("top")
"""
class FavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # 有料会員かどうか確認
        if not PremiumUser.objects.filter(user=request.user).exists():
            return HttpResponseForbidden("有料会員のみお気に入り登録ができます。")

        # レストランを取得
        restaurant = Restaurant.objects.filter(id=pk).first()

        # 既にお気に入りに登録されているかチェック
        existing_favorite = Favorite.objects.filter(user=request.user, restaurant=restaurant).first()

        if existing_favorite:
            # 既にお気に入りに登録されている場合は解除（削除）
            existing_favorite.delete()
            print("お気に入りを解除しました。")
        else:
            # まだお気に入りに登録されていない場合は新規登録
            copied = request.POST.copy()
            copied["user"] = request.user
            copied["restaurant"] = restaurant

            form = FavoriteForm(copied)
            if form.is_valid():
                form.save()
                print("お気に入りに登録しました。")
            else:
                print(form.errors)

        # お気に入りの状態に応じてレストラン詳細ページにリダイレクト
        return redirect("restaurant", pk=pk)



"""class ReservationView(LoginRequiredMixin,View):
    def post(self, request,pk):

        restaurant = Restaurant.objects.filter(id=pk).first()   
        copied = request.POST.copy()
        copied["user"] = request.user
        copied["restaurant"] = restaurant


        form = ReservationForm(copied)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print(form.errors)

        return redirect("top")
"""
class ReservationView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # 有料会員かどうか確認
        if not PremiumUser.objects.filter(user=request.user).exists():
            return HttpResponseForbidden("有料会員のみご利用いただけます。")

        # レストランを取得
        restaurant = get_object_or_404(Restaurant, id=pk)

        # フォームデータをPOSTからコピーし、userとrestaurantを追加
        form_data = request.POST.copy()
        form_data.update({
            "user": request.user,
            "restaurant": restaurant
        })

        # フォームインスタンスを作成
        form = ReservationForm(form_data)

        # フォームが有効な場合、保存し、トップページにリダイレクト
        if form.is_valid():
            form.save()
            return redirect("top")
        else:
            print(form.errors)  # デバッグ用エラーメッセージ
            return render(request, "reservation.html", {"form": form, "restaurant": restaurant})


class MypageView(LoginRequiredMixin,View):
    def get(self, request):

        context = {}

        context["favorites"] = Favorite.objects.filter(user=request.user)
        context["reviews"] = Review.objects.filter(user=request.user)
        context["reservations"] = Reservation.objects.filter(user=request.user)

        context["is_premium"] = PremiumUser.objects.filter(user=request.user).exists()
        return render(request, "mypage.html", context)
    
    def post(self, request):

        request.user.first_name = request.POST["first_name"]
        request.user.last_name = request.POST["last_name"]


        return redirect("mypage")



class CheckoutView(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):

        
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': settings.STRIPE_PRICE_ID,
                    'quantity': 1,
                },
            ],
            payment_method_types=['card'],
            mode='subscription',

        
            success_url=request.build_absolute_uri(reverse_lazy("success")) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse_lazy("mypage")),
        )

        
        print( checkout_session["id"] )

        return redirect(checkout_session.url)


class SuccessView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):

        print("有料会員登録しました！")


        if "session_id" not in request.GET:
            print("セッションIDがありません。")
            return redirect("mypage")


        try:
            checkout_session_id = request.GET['session_id']
            checkout_session    = stripe.checkout.Session.retrieve(checkout_session_id)
        except:
            print( "このセッションIDは無効です。")
            return redirect("mypage")

        print(checkout_session)

        if checkout_session["payment_status"] != "paid":
            print("未払い")
            return redirect("mypage")

        print("支払い済み")

        premium_user = PremiumUser()
        premium_user.user = request.user
        premium_user.premium_code = checkout_session["customer"]
        premium_user.save()


        return redirect("mypage")


# 有料会員の設定
class PortalView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):

        # userフィールドが自分(request.user)の有料会員情報(PremiumUser)を取り出す
        premium_user = PremiumUser.objects.filter(user=request.user).first()

        if not premium_user:
            print( "有料会員登録されていません")
            return redirect("mypage")

        try:
        # ユーザーモデルに記録しているカスタマーIDを使って、ポータルサイトへリダイレクト
            portalSession   = stripe.billing_portal.Session.create(
                customer    = premium_user.premium_code,
                return_url  = request.build_absolute_uri(reverse_lazy("mypage")),
            )

            return redirect(portalSession.url)
        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)



class PremiumView(View):
    def get(self, request, *args, **kwargs):
        
        premium_user = PremiumUser.objects.filter(user=request.user).first()


        if not premium_user:
            print("カスタマーIDがセットされていません。")
            return redirect("mypage")

        try:
            subscriptions = stripe.Subscription.list(customer=premium_user.premium_code)
        except:
            print("このカスタマーIDは無効です。")
            premium_user.delete()

            return redirect("mypage")


        is_premium = False

        for subscription in subscriptions.auto_paging_iter():
            if subscription.status == "active":
                print("サブスクリプションは有効です。")
                is_premium = True

        if is_premium:
            print("有料会員です")
        else:
            print("有料会員ではない")

        return redirect("mypage")


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # レビューを取得
        review = get_object_or_404(Review, pk=pk)

        # レビューの投稿者が現在のユーザーでない場合はエラーを返す
        if review.user != request.user:
            return HttpResponseForbidden("このレビューを編集する権限がありません。")

        # 有料会員でない場合もエラー
        if not PremiumUser.objects.filter(user=request.user).exists():
            return HttpResponseForbidden("有料会員のみレビューを編集できます。")

        form = ReviewForm(instance=review)
        return render(request, "edit_review.html", {"form": form , "review":review})

    def post(self, request, pk):
        # レビューを取得
        review = get_object_or_404(Review, pk=pk)

        # レビューの投稿者が現在のユーザーでない場合はエラーを返す
        if review.user != request.user:
            return HttpResponseForbidden("このレビューを編集する権限がありません。")

        # 有料会員でない場合もエラー
        if not PremiumUser.objects.filter(user=request.user).exists():
            return HttpResponseForbidden("有料会員のみレビューを編集できます。")

        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            return redirect("mypage")  # 編集後にマイページにリダイレクト
        return render(request, "edit_review.html", {"form": form, "review":review})

class DeleteReviewView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # レビューを取得
        review = get_object_or_404(Review, pk=pk)

        # レビューの投稿者が現在のユーザーでない場合はエラーを返す
        if review.user != request.user:
            return HttpResponseForbidden("このレビューを削除する権限がありません。")

        # 有料会員でない場合もエラー
        if not PremiumUser.objects.filter(user=request.user).exists():
            return HttpResponseForbidden("有料会員のみレビューを削除できます。")

        # レビュー削除
        review.delete()
        return redirect("mypage")

class EditProfileView(View):
    def get(self, request):
        # ユーザーのプロフィール情報を取得し、フォームに渡す
        form = UserProfileForm(instance=request.user)

        context = {
            'form': form
        }

        return render(request, "edit_profile.html", context)

    def post(self, request):
        # フォームをPOSTデータで初期化
        form = UserProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            # フォームが有効な場合
            new_password = form.cleaned_data.get('password')
            if new_password:
                # パスワードが変更された場合
                request.user.set_password(new_password)
                request.user.save()
                # セッションの認証情報を更新
                update_session_auth_hash(request, request.user)
            else:
                # パスワードが変更されていない場合は、他の情報を保存
                form.save()

            # 更新後、マイページにリダイレクト
            return redirect('mypage')

        # フォームが無効な場合、再度フォームを表示
        return render(request, "edit_profile.html", {'form': form})

def mypage_view(request):
    # プレミアム会員情報を取得
    is_premium = PremiumUser.objects.filter(user=request.user, is_active=True).exists()

    context = {
        'favorites': Favorite.objects.filter(user=request.user),
        'reviews': Review.objects.filter(user=request.user),
        'reservations': Reservation.objects.filter(user=request.user),
        'is_premium': is_premium,  # プレミアム会員かどうかを渡す
    }

    return render(request, 'mypage.html', context)

class CancelPremiumView(View):
    def get(self, request):
        # 処理内容
        return render(request, 'mypage.html') 