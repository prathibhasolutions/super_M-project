from django.http import HttpResponse
from django.template import loader
from .models import Item, profit, Members, Dealer
from django.shortcuts import render, redirect
from functools import wraps
from functools import wraps


def custom_login_required(view_func):
  @wraps(view_func)
  def _wrapped_view(request, *args, **kwargs):
    if not request.session.get('is_authenticated', False):
      return redirect('login')
    return view_func(request, *args, **kwargs)
  return _wrapped_view

@custom_login_required
def items(request): 
  all_items = Item.objects.all().select_related('dealer')
  profit2 = profit.objects.get(name = "Overall")
  template = loader.get_template('all_items.html')
  total_finance = 0
  profit2 =profit2.total 
  for item in all_items:
    price=item.price or 0.00
    quantity=item.quantity or 0
    total_finance+=price*quantity
              
  context = {
    'all_items': all_items,
    'total_finance':total_finance,
    'profit':profit2,
  }
  return HttpResponse(template.render(context, request)) 

@custom_login_required 
def details(request, id):
  all_items = Item.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'all_items': all_items,
    
  }
  return HttpResponse(template.render(context, request))

@custom_login_required
def main(request):
  
  return render(request, 'main.html')


@custom_login_required
def dealer(request):
  if request.method=="POST":
    dealer_name=request.POST.get('dealer_name')
    dealer_phNo=request.POST.get('delaer_phNo')
    dealer_add=request.POST.get('dealer_add')

    Dealer.objects.create(dealer_name=dealer_name, dealer_phNo=dealer_phNo, dealer_add=dealer_add)
    return redirect('main')
  return render(request, 'dealer.html') 

@custom_login_required
def create(request):
  if request.method=="POST":
    date_arrived=request.POST.get('date_arrived')
    product_name=request.POST.get('product_name')
    price=request.POST.get('price')
    quantity=request.POST.get('quantity')
    expiry_date=request.POST.get('expiry_date')
    dealer_id = int(request.POST.get('dealer'))
    dealer = Dealer.objects.get(id = dealer_id)

    Item.objects.create(date_arrived=date_arrived, product_name=product_name, price=price, quantity=quantity, expiry_date=expiry_date, dealer=dealer )
    return redirect('main')
  
  dealer_s = Dealer.objects.all().values()
  context = {
    'dealer_s': dealer_s,
  }
  return render(request, 'create_item.html', context)

@custom_login_required
def update(request):
  if request.method=="POST":
    product_name=request.POST.get('products')
    try:
      item=Item.objects.get(product_name=product_name)
    except Item.DoesNotExist:
      return HttpResponse("Item not found")
    
    qty=int(request.POST.get('quantity'))
    selling_price=float(request.POST.get('selling_price') or 0.00)
    buying_price=float(item.price or 0.00)

    overall_profit = profit.objects.get(name = "Overall")
    overall_profit.total += (selling_price-buying_price)*qty
    
    item.quantity-=qty
    overall_profit.save()
    item.save()

    return redirect('items')
  all_items = Item.objects.all().values()
  context = {
    'all_items':all_items,
  }
  return render(request, 'update.html', context)


def login(request):
  if request.method=="POST":
    user_name=request.POST.get('username')
    pass_word=request.POST.get('password')
    members=Members.objects.all().values()
    for x in members:
      if x['username']==user_name and x['password']==int(pass_word):
        request.session['is_authenticated'] = True
        request.session['username'] = user_name
        return redirect('main')
      
    template = loader.get_template('login.html')
    context = {
      'message': "Username or Password is wrong, try again",
    
    }
    return HttpResponse(template.render(context, request))
    
    
  return render(request, 'login.html')

def logout(request):
  request.session.flush()
  return redirect('login')