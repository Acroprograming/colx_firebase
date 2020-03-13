import pyrebase 
from django.shortcuts import render ,get_object_or_404
from django.template import loader
from django.http import HttpResponse ,HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import ast


config = {
	'apiKey': "AIzaSyAdVcfPtjrubR5foi9kuvK_1-2NrNahaUo",
    'authDomain': "colx-b25d8.firebaseapp.com",
    'databaseURL': "https://colx-b25d8.firebaseio.com",
    'projectId': "colx-b25d8",
    'storageBucket': "colx-b25d8.appspot.com",
    'messagingSenderId': "663148072979",
    'appId': "1:663148072979:web:fbd081dc36db06cdfeefe6",
    'measurementId': "G-G1BZHPGXL6"

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage=firebase.storage()
def login(request):
	if(request.method=='POST'):
		email=request.POST.get('email')
		passw = request.POST.get("password")
		try:
			user = auth.sign_in_with_email_and_password(email,passw)
		except:
			message = "invalid cerediantials"
			return render(request,"colx_firebase/login.html",{"msg":message})
		request.session['localId']=str(user['localId'])
		request.session['idToken']=str(user['idToken'])
		#print(user)
		return HttpResponseRedirect(reverse('colx_firebase:index'))
	else:
		return render(request,"colx_firebase/login.html")

def logout(request):
	try:
		del request.session['localId']
		del request.session['idToken']
		#del request.session['roll_number']
	except KeyError:
		pass
	return HttpResponseRedirect(reverse('colx_firebase:index'))

def index(request):
	items=db.child("items").get()
	try:
		useritems=items.val()
		#print(useritems)
		for users in useritems.keys():
		#print(l[x])
			for item in useritems[users].values():
				#print(item['description'])
				pass
		return render(request, "colx_firebase/index.html",{'useritems':useritems})
	except:
		return render(request,"colx_firebase/index.html")
		#items=items.val()
	#print(items)
	'''if(items):
						data=items.each()
						items=items
						print(items.val())
						for x,y in items(items.val()):
							print(x)
							print(y)
						if(data):
							for a in data:	
								#print(a.val())
								for y in a.val():
									#print('item=',y)
									#print(a.val()[y]['item name'])
									items=a.val()
									#print(items)
					'''	
	'''for x in items.each():
		print("x ",x.key())'''
		
	
'''def add_to_cart(request,item_id):
	item=db.child("item").child(item_id).get()
	items=item.val()
	db.child("cart").child(item_id).set()
'''
def cart(request):
	localId=request.session['localId']
	items=db.child("student").child(localId).child("cart").get()
	try:
		useritems=items.val()
		#print(useritems)
		for users in useritems.keys():
		#print(l[x])
			for item in useritems[users].values():
				#print(item['description'])
				pass
		return render(request, "colx_firebase/cart.html",{'useritems':useritems})
	except:
		return render(request,"colx_firebase/cart.html")
def add_to_cart(request):
	try:
		localId=request.session['localId']
		#seller_obj=db.child("student").order_by_child("email")equal_to(email).get()
	except KeyError:
		err="You need to login first to Sell any item"
		return render(request,'colx_firebase/login.html',{'msg':err})
	else:
		if(request.method=="POST"):
			seller=request.POST['seller']
			item=request.POST['item']
			itemkey=request.POST['itemkey']
			#print(itemkey)
		db.child("student").child(localId).child("cart").child(seller).child(itemkey).set(ast.literal_eval(item))
		#print("add_to_cart")
		return HttpResponseRedirect(reverse('colx_firebase:index'))
def buy(request,userid,itemid):
	try:
		localId=request.session['localId']
	except KeyError:
		err="You need to login first to Buy any item"
		return render(request,'colx_firebase/login.html',{'msg':err})
	else:
		seller=db.child("student").child(userid).child("details").get()
		seller=seller.val()
		item=db.child("items").child(userid).child(itemid).get()
		item=item.val()
		#print(seller)
		#print(item)
		return render(request,'colx_firebase/buy.html',{'seller':seller,'item':item})
def signup(request):
	#return render(request,"colx_firebase/signup.html")
	if(request.method =='POST'):
		fname=request.POST['fname']
		lname=request.POST['lname']
		roll_number=request.POST['roll_number']
		year=request.POST['year']
		class_field=request.POST['class_field']
		section=request.POST['section']
		password=request.POST['password']
		mobile_number=request.POST['mobile_number']
		email=request.POST['email']
		try:
			user=auth.create_user_with_email_and_password(email,password)
		except Exception as e:
			return render(request, "colx_firebase/signup.html",{'msg':e})
		
		student={'first_name':fname,'last_name':lname,'email':email,'year':year,'class':class_field,'mobile_number':mobile_number,'section':section}
		
		db.child("student").child(user['localId']).child("details").set(student)

		return HttpResponseRedirect(reverse('colx_firebase:index'))
	else:		
		return render(request,"colx_firebase/signup.html")
def sell(request):
	#user = db.child("student").order_by_child("email").get()
	#ki=user.val()
	#student = db.child("student").order_by_child("email").equal_to("acroprograming@gmail.com").get()# users
	#return HttpResponse("user.val()" + str(ki) +" user"+str(user))
	
	#seller=db.child("student").order_by_child("email")equal_to(email).get()
	#print(seller)
	try:
		localId=request.session['localId']
		#seller_obj=db.child("student").order_by_child("email")equal_to(email).get()
	except KeyError:
		err="You need to login first to Sell any item"
		return render(request,'colx_firebase/login.html',{'msg':err})
	else:
		if(request.method=='POST'):
			img=request.FILES['img']
			item_name=request.POST['item_name']
			price=request.POST['price']
			description=request.POST['description']
			img_name=item_name+localId+img.content_type
			'''fs = FileSystemStorage()
			filename=fs.save(item_name+localId+img.content_type,img)
			uploaded_file_url = fs.url(filename)'''
			storage.child("item images/"+img_name).put(img)
			uploaded_file_url=storage.child("item images/"+img_name).get_url(request.session['idToken'])
			#seller_obj=Student.objects.get(id=request.session["id"])
			item={'item_name':item_name,'price':price,'img':uploaded_file_url,'status':'not sold','description':description,'seller':localId}
			#item.save()
			db.child("items").child(localId).push(item)
			return HttpResponseRedirect(reverse('colx_firebase:index'))
		return render(request,'colx_firebase/sell.html')
	return HttpResponseRedirect(reverse('colx_firebase:index'))


























