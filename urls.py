from django.urls import path

from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MySetPasswordForm, MypasswordChangeForm

urlpatterns = [
    path('',views.home),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path("category/<slug:val>",views.CategoryView.as_view(),name="category"),
    path("category-title/<val>",views.CategoryTitle.as_view(),name="category-title"),
    path("product-detail/<int:pk>",views.ProductDetail.as_view(),name="product-detail"),
    path("profile/",views.ProfileView.as_view(),name="profile"),
    path("address/",views.address,name="address"),
    path("updateAddress/<int:pk>",views.updateAddress.as_view(),name="updateAddress"),

    #Login Authentication  of Change Password
    path("registration/",views.CustomerRegistrationView.as_view(),name="customerregistration"),

    path("accounts/login/",auth_view.LoginView.as_view(template_name ='app/login.html',authentication_form =LoginForm), name="login"),

    path("add-to-cart/", views.add_to_cart,name='add-to-cart'),

    path("cart/",views.show_cart,name="showcart"),

    path("checkout/",views.checkout.as_view(),name="checkout"),

    #Payment done will be connected to the razorpay
    path("paymentdone/",views.payment_done,name="paymentdone"),
    
    #order details after payment done
    path("orders/",views.orders,name="orders"),

    #order after feedback form .......
    path('feedback/<int:pk>/',views.feedback_form, name='feedback_form'),

     # Search bar in action with the held by the all the unit
    path('search/',views.search,name='search'),

    # Wishlist in action with show by the url
    path('wishlist/',views.show_wishlist,name='showwishlist'),


    #For the add,minus and remove from the cart   
    path("pluscart/",views.plus_cart),
    path("minuscart/",views.minus_cart),
    path("removecart/",views.remove_cart),

    path("pluswishlist/",views.plus_wishlist),
    path("minuswishlist/",views.minus_wishlist),
   

    

    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name ='app/changepassword.html',form_class=MypasswordChangeForm, success_url ='/passwordchangedone'),name='passwordchange'),

    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name ='app/passwordchangedone.html'),name='passwordchangedone'),

    path('logout/',views.logout,name='logout'),
    # path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),


    #Forget Password with the Details for change password
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name ='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),

    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name ='app/password_reset_done.html'),name='password_reset_done'),
 
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name ='app/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name ='app/password_reset_complete.html'),name='password_reset_complete'),

    path('test/<int:pk>/',views.generate_pdf),

    #crud operations
    path('Pro', views.Pro),  
    path('show',views.show),  
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),  
    path('delete/<int:id>', views.destroy),  

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Krafitech Pvt.Ltd."
admin.site.site_title = "Krafitech Pvt Ltd"
admin.site.site_index_title = "Krafitech Resto Management"

