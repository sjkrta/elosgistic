from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('reset/', views.reset_view, name='reset'),
    path('logout/', views.logout_view, name='logout'),
    path('browse/', views.categories_view, name='browse'),
    path('sales/', views.sales_view, name='sales'),
    path('category/<int:category>/', views.category_view, name='category'),
    path('product/<int:productId>/', views.product_view, name='product'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('cost/calculator/', views.cost_calculator_view, name ='cost_calculator'),
    path('tracking/', views.tracking, name ='tracking'),
    path('shipping/', views.shipping, name = 'shipping'),
    path('thankyou/', views.thankyou, name = 'thankyou'),
    path('aboutus/', views.aboutus, name = 'aboutus'),
    path('support/', views.support, name = 'support'),
    path('support/thankyou/', views.thankyouSupport, name = 'thankyou_support'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header  =  "Estorage Admin Site"  
admin.site.site_title  =  "Estorage"
admin.site.index_title  =  "Admin"