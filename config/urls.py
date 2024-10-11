from django.contrib import admin
from django.urls import path,include
from nagoyameshi.views import TopView,RestaurantView,ReviewView,FavoriteView,ReservationView,MypageView,SuccessView,CheckoutView,PremiumView,PortalView,CancelReservationView,EditReviewView, DeleteReviewView,EditProfileView,CancelPremiumView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",TopView.as_view(), name="top"),
    path("restaurant/<int:pk>/",RestaurantView.as_view(), name="restaurant"),
    path("review/<int:pk>/",ReviewView.as_view(), name="review"),
    path("favorite/<int:pk>/",FavoriteView.as_view(), name="favorite"),
    path("reservation/<int:pk>/", ReservationView.as_view(), name="reservation"),
    
    path("mypage/", MypageView.as_view(), name="mypage"),

    path("success/", SuccessView.as_view(), name="success"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("premium/", PremiumView.as_view(), name="premium"),
    path("portal/", PortalView.as_view(), name="portal"),
    path('reservation/cancel/<int:pk>/', CancelReservationView.as_view(), name='cancel_reservation'),
    path('accounts/', include('allauth.urls')),
    path('review/edit/<int:pk>/', EditReviewView.as_view(), name='edit_review'),
    path('review/delete/<int:pk>/', DeleteReviewView.as_view(), name='delete_review'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    path('cancel-premium/', CancelPremiumView.as_view(), name='cancel_premium'),
]

