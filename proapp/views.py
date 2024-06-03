
from django import forms
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Cart, Order, Room , Product, Topic, Message
from .forms import RoomForm 
from django.db.models import Q
import razorpay
from django.core.mail import send_mail
# from mailbox import Message
def index(request):
    room = None
    room = Room.objects.all()
    context = {}
    context['data'] = room
    return render(request , 'home.html',context)

   
    
# def base(request):
#     return render(request,'base.html')
  
 
context = {}
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        un = request.POST['uname']
        ue = request.POST['username']
        p = request.POST['upass']
        cp = request.POST['ucpass']
        # print(un)
        # print(ue)
        # print(p)
        # print(cp)
        
        if un == '' or ue == '' or p =='' or cp == '':
            context['errmsg']='feild cant be blank '
            return render(request, 'signup.html',context)
        elif p != cp:
            context['errmsg']='password and confirm passsword should be same'
            return render(request, 'signup.html',context)
        elif len(p) < 8:
            context['errmsg']='password should be greater than 8..'
            return render(request, 'signup.html',context)
        else:
            m = User.objects.create(username = un)
            m.set_password(p)    ## for password encription
            m.save()
            context['success']='Data inserted succesfully........!'
            return render(request, 'signup.html',context)
            

def ulogin(request):
    context = {}
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        n = request.POST['uname']
        p = request.POST['upass']
        # print(n)
        # print(p)
        e = authenticate(username=n,password=p)
        # print(e)
        if e is not None:
            login(request,e)
            return redirect('/home')
        else:
            context['ermsg']='Invalid Username or Password'
            return redirect(request,'/login')
        
def ulogout(request):
    logout(request)
    return redirect('/home')

    #   <img style="height: 10rem; width: 20rem; margin: auto;" src="{% static 'images/logo11.png' %}" alt="logo">


# def home(request):
#     rooms = Room.objects.all()
#     context['data'] = rooms
#     return render(request,'index.html',context )


# def room(request , pk):
#     room = None
#     room = Room.objects.get(id = pk)
#     context = {}
#     context['data'] = room
#     return render(request, 'home.html', context)


# def room(request):
#     return render(request, 'room.html')




def sample(request):
    room = None
    room = Room.objects.all()
    context = {}
    context['data'] = room
    return render(request , 'sample.html',context)


# @login_required(login_url='/login')
# def CreateRoom(request):
#     form = RoomForm()
#     topics = Topic.objects.all()
#     if request.method == 'POST':
#         # topics_name = request.POST.get('topic')
#         # topic , created = Topic.objects.get_or_create(name = topics_name  )

#         rn = request.POST['topic']
#         t = request.POST['name']
#         d = request.POST['description']
#         m = Room.objects.create(topic=rn, name=t, description=d  )
#         m.save()
#         return redirect('/home')

        # form = RoomForm(request.POST)
        # Room.objects.create(
        #     host = request.user,
        #     topic = topic,
        #     name = request.POST.get('name'),
        #     description = request.POST.get('description')

        # )
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     return redirect('/home')

    # context = {'from':form, 'topics': topics  }
    
    # return render(request, 'create-room.html', context)

@login_required(login_url='/login')
def CreateRoom(request):
    form = RoomForm()
 
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('/home')

    context = {'form': form, }
    return render(request, 'create-room.html', context)


# def UpdateRoom(request, pk):
#     room = Room.objects.get(id = pk )
#     form = RoomForm(instance = room)
#     topics = Topic.objects.all()

#     context ={'from': form, 'topics': topics }
#     return render (request, 'create-room.html',context)


# def UpdateRoom(request, pk):
#     form = RoomForm(request.POST, instance=room)
#     if form.is_valid():
#         form.save()
#         return redirect('/home')
#     context = {'form':form}
#     return render(request, 'create-room.html',context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('/home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'create-room.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # rooms = Room.objects.filter(topic__name__icontains = q)

    rooms = Room.objects.filter(
       
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )    ## for browse topic and search the room

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics': topics,'room_messages': room_messages,
               'room_count': room_count,}
    return render(request, 'home.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'profile.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        # return redirect('/home', pk=room.id)
        return redirect(reverse('room', kwargs={'pk': room.id}))
        
        

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'room.html', context)


@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('/home')
    return render(request, 'delete.html', {'obj': room})


@login_required(login_url='/login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')
    if request.method == 'POST':
        message.delete()
        return redirect('/home')
    return render(request, 'delete.html', {'obj': message})



# @login_required(login_url='/login')
# def delete(request,pk):
#     room = Room.objects.get(id=pk)
#     context= {'room':room }
#     return request(render, 'delete.html',context)







############  courses part ##################

def courses(request):
    p = Product.objects.all()
    context = {}
    context['data']= p
    return render(request, 'courses.html',context)

def fetchorder(request):
    o = Order.objects.filter(uid = request.user.id)
    context = {}
    tamount= o
    context['data']=o
    context['total']=tamount
    return render(request,'placorder.html',context)

def placeorder(request):
    c=Cart.objects.filter(uid=request.user.id)
    for i in c:
        amount=i.qty*i.pid.price
        o=Order.objects.create(uid=i.uid,pid=i.pid,qty=i.qty,price=amount)
        o.save()
        i.delete()
         
    return redirect('/fetchorder')
    

# def viewcard(request):
#     return render (request,'viewcard.html')

def product_detail(request, pid):
    context = {}
    p = Product.objects.filter(id=pid)
    context['data'] = p
    return render(request,'viewcard.html',context)


def makepayment(request,uid):
    client = razorpay.Client(auth=("rzp_test_IC8L83MtJlRjzB", "8IYbz2xMiHDD1W3D9yWUBKUB")) 
    o = Product.objects.filter(id = uid)
    s = 0
    for i in o:
        s =s +i.price
   
    data = { "amount": s*100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    # print(payment)
    context['payment'] = payment
    return render(request,'pay.html',context)


def orderc(request, uid):
    p = Cart.objects.filter(id = request.user.id)
    p.save()
    context= {'data':p}
    return render(request, 'paymentsuccess.html',context)
    


def paymentsucess(request):
    u=User.objects.filter(id=request.user.id)
    to=u[0].email
    sub='Payment Success'
    msg='Thanks for Shopping...!!!!'
    frm='hrikeshyadav1999@gmail.com'
    send_mail(
        sub,
        msg,
        frm,
        [to],
        fail_silently=False
    )
    return render(request,'paymentsuccess.html')

