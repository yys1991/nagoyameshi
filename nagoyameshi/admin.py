"""from django.contrib import admin

# == This code was created by https://noauto-nolife.com/post/django-auto-create-models-forms-admin/== #

from django.contrib import admin
from .models import Category,Restaurant,Review,Favorite,Reservation,PremiumUser

class CategoryAdmin(admin.ModelAdmin):
    list_display	= [ "id", "name", "created_at", "updated_at" ]

class RestaurantAdmin(admin.ModelAdmin):
    list_display	= [ "id", "category", "name", "image", "description", "start_at", "end_at", "cost", "post_code", "address", "tel", "created_at", "updated_at" ]

class ReviewAdmin(admin.ModelAdmin):
    list_display	= [ "id", "restaurant", "user", "content", "created_at", "updated_at" ]

class FavoriteAdmin(admin.ModelAdmin):
    list_display	= [ "id", "user", "restaurant", "created_at" ]

class ReservationAdmin(admin.ModelAdmin):
    list_display	= [ "id", "user", "restaurant", "datetime", "headcount", "created_at", "updated_at" ]

class PremiumUserAdmin(admin.ModelAdmin):
    list_display	= [ "id", "user", "premium_code" ]


admin.site.register(Category,CategoryAdmin)
admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Favorite,FavoriteAdmin)
admin.site.register(Reservation,ReservationAdmin)
admin.site.register(PremiumUser,PremiumUserAdmin)
"""
from django.contrib import admin
from .models import Category, Restaurant, Review, Favorite, Reservation, PremiumUser

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at", "updated_at"]
    search_fields = ['name']  # カテゴリ名で検索できるようにする

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "name", "image", "description", "start_at", "end_at", "cost", "post_code", "address", "tel", "created_at", "updated_at"]
    search_fields = ['name', 'category__name']  # 店舗名とカテゴリ名で検索できるようにする

class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "restaurant", "user", "content", "created_at", "updated_at"]
    search_fields = ['restaurant__name', 'user__username', 'content']  # レビューに対しても検索可能にする

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "restaurant", "created_at"]
    search_fields = ['user__username', 'restaurant__name']  # ユーザー名と店舗名で検索できるようにする

class ReservationAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "restaurant", "datetime", "headcount", "created_at", "updated_at"]
    search_fields = ['user__username', 'restaurant__name']  # 予約に対してもユーザー名と店舗名で検索

class PremiumUserAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "premium_code"]
    search_fields = ['user__username', 'premium_code']  # プレミアムユーザーの検索

# モデルの登録
admin.site.register(Category, CategoryAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(PremiumUser, PremiumUserAdmin)
