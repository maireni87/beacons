from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission

from shopping_cart.models import Store, Item, Order, Transaction
from view_functions import add_item, chart_prep

#### Stores ##########
@login_required
def home(request):
	stores = Store.objects.all()
	return render(request, 'templates/select_store.html', {'stores': stores})

@login_required
def store_homepage(request, store_id, ordered=False):
	# get the store's name from the subdomain or the passed store id. 
	try:
		#s = get_object_or_404(Store, name='Guitar Store')
		s = get_object_or_404(Store, name=request.subdomain) 
		Items = Item.objects.all().filter(store=s)
		
	except:
		s = get_object_or_404(Store, pk=store_id) 
		Items = Item.objects.all().filter(store=s)
	shipping_choices = Order.shipping_choices
	return render(request, "templates/store_homepage.html", {
		'Items':Items, 
		'ordered':ordered, 
		'shipping_choices':shipping_choices
		})


##### Handel login / logout #######
def logout_view(request):
    logout(request)

def create_user(request):
	'''
	create and login user
	'''
	if request.method == 'POST':
		form = UserCreationForm(request.POST)	
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password2')
			form.save()
			#login user
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
			    	return HttpResponseRedirect('/')
	else:
		form = UserCreationForm()
	return render(request, 'templates/create_user.html', {'form': form})

### shopping_cart ###
@login_required
def add_to_cart(request):
	if request.method == "POST":
		item_id = add_item(request)
		i = Item.objects.get(pk=item_id)
		return store_homepage(request, i.store.id, ordered=True)

@login_required
def inline_add_to_cart(request):
	if request.method == "POST":
		add_item(request)
		return view_cart(request)

@login_required
def view_cart(request): 
	recommendations = Transaction.objects.filter(order=Order.objects.filter(buyer=request.user)[0])[0].recommend
	shipping_choices = Order.shipping_choices
	if request.session.get('cart', default=None) != None:
		data = chart_prep(request.session.get('cart'))

		return render(request, "templates/cart.html", {
			'cart_items': request.session['cart'], 
			'recommendations':recommendations,
			'shipping_choices':shipping_choices,
			'data':data
			})
	else:
		return render(request, "templates/empty_cart.html", {'recommendations':recommendations, 'shipping_choices':shipping_choices})

def checkout(request):
	if request.method == "GET":
		# Create order first
		o = Order.objects.create(buyer=request.user)
		# add items to order
		for i in request.session['cart']:
			Transaction.objects.create(
				order = o, 
				item=Item.objects.get(pk=i['item_id']), 
				quantity=i['quantity']
				)
		# empty cart
		del request.session['cart']
		return render(request, "templates/order_processed.html", {'order': o})

def previous_orders(request):
	p_orders = Order.objects.all().filter(buyer=request.user).order_by('date_ordered').reverse()
	return render(request, "templates/previous_orders.html", {'p_orders':p_orders})
