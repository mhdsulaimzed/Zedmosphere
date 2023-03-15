from store.models import Cart
from django.contrib.auth import authenticate
def cart_count(request):
    if request.user.is_authenticated:
        cnt=Cart.objects.filter(user=request.user,status="in-cart").count()
    else:
        cnt=0

    return{"count":cnt}

    