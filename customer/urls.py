from django.urls import path
from customer import views

urlpatterns = [
    path('signup',views.SignupView.as_view(),name="sign-up"),
    path('signin',views.SigninView.as_view(),name="log-in"),
    path('home',views.IndexView.as_view(),name="home"),
    path("product/<int:id>",views.ProductDetailView.as_view(),name="product-detail"),
    path("products/<int:id>/cart/add",views.AddToCartView.as_view(),name="cart-add"),
    path("products/mycart",views.CartList.as_view(),name="cart-list"),
    path("products/<int:id>/mycart/change",views.CartRemoveView.as_view(),name='remove-cartitem'),
    path("products/mycart/checkoutsingle/<int:id>",views.MakeorderView.as_view(),name="make-single-order"),
    path("order/all",views.MyOrderView.as_view(),name="my-order"),
    path("order/<int:id>/change",views.OrderCancelView.as_view(),name="cancel-order"),
    path("offers/products",views.DiscountView.as_view(),name="offer-products"),
    path("product/review/<int:id>",views.ReviewCreateView.as_view(),name="add-review"),
    path("logout",views.sign_out_view,name="log-out")
]
