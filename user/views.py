from django.shortcuts import render,redirect
from myadmin.models import Area,Category,Product,City,Inquiry,Profile,Post,Feedback,Quickcontact,Comment,Likes,Report
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import auth,messages
import os
from django.http import HttpResponse


def home(request):
    context = {}
    return render(request,'user/home.html',context)
def about_us(request):
    context = {}
    return render(request,'user/about_us.html',context)
def error(request):
    context = {}
    return render(request,'user/error.html',context)
# registration
def register(request):
   
    area=Area.objects.all()
    context = {'area':area}
    return render(request,'user/register.html',context)

def store_profile(request):
    fname     = request.POST['fname']
    lname     = request.POST['lname']
    email     = request.POST['email']
    username  = request.POST['username']
    password  = request.POST['password']
    cpassword = request.POST['cpassword']
    dob       = request.POST['dob']
    area      = request.POST['area']
 
    contact   = request.POST['contact']
    address   = request.POST['address']

    result = User.objects.filter(username=username)
    print(result)

    if result.exists():
        messages.error(request, 'Username already exists')
        return redirect('/user/register/')
    else:
        
        if password == cpassword:
            user = User.objects.create_user(first_name=fname,last_name=lname,email=email,username=username,password=password)
            Profile.objects.create(contact=contact, address=address,dob=dob,area_id=area, user_id=user.id)
            return redirect('/user/login/')
        else:
            messages.error(request, 'Password Missmatch')
            return redirect('/user/register/')
   
    
#Edit Profile
def edit_profile(request):
    area=Area.objects.all()
    id = request.user.id
    result=  Profile.objects.get(user_id=id)
    result1=  User.objects.get(pk=id)
    context={'result':result, 'result1':result1,'area':area}
    return render(request,'user/edit_profile.html',context)
def update_profile(request,id):
    fname     = request.POST['fname']
    lname     = request.POST['lname']
    email     = request.POST['email']
    # username  = request.POST['username']
    password  = request.POST['password']
    cpassword = request.POST['cpassword']

    dob       = request.POST['dob']
    area      = request.POST['area']
    contact   = request.POST['contact']
    address   = request.POST['address']
    data = {
               'cpassword':cpassword,
               'dob' : dob,
               'area_id':area,
               'contact':contact,
               'address':address,
           }
    if password == cpassword:
       user=User.objects.update_or_create(pk=request.user.id, defaults={'first_name':fname,'last_name':lname,'email':email})
       Profile.objects.update_or_create(pk=id, defaults=data)
       return redirect('/user/profile/')
    else:
        messages.error(request, 'Password Missmatch')
        return redirect('/user/edit_profile/')

    # result = User.objects.filter(username=username)
    # print(result)

    # if result.exists():
    #     messages.error(request, 'Username already exists')
    #     return redirect('/user/edit_profile/')
    # else:
        
    #     if password == cpassword:
    #         Profile.objects.update_or_create(pk=id, defaults=data)
    #         return redirect('/user/profile/')
    #     else:
    #         messages.error(request, 'Password Missmatch')
    #         return redirect('/user/edit_profile/')

    
# login process
def login(request):
    context = {}
    return render(request,'user/login.html',context)
def login_check(request):
    myusername = request.POST['username']
    mypassword = request.POST['password']

    result = auth.authenticate(username=myusername, password=mypassword)

    if result is None:
        messages.error(request, 'Invalid Username or Password')
        return redirect('/user/login/')
    else:
        auth.login(request, result)
        return redirect('/user/home/')


def logout(request):
    auth.logout(request)
    return redirect('/user/login/')
def security(request):
    context = {}
    return render(request,'user/security.html',context)
#contact us CRUD
def contact_us(request):
    context = {}
    return render(request,'user/contact_us.html',context)
def store_contact(request):
    name    = request.POST['name']
    email = request.POST['email']
    message    = request.POST['message']
    Inquiry.objects.create(name=name,email=email,message=message)
    return redirect('/user/contact_us/')

def security(request):
    result = Product.objects.all()
    context = {'result':result}
    return render(request,'user/security.html',context)
    
def store_feedback(request):
    message  = request.POST['message']
    rating =request.POST['rating']
    id=request.user.id
    user=User.objects.get(pk=id)
    Feedback.objects.create(message=message,rating=rating,user_id=user.id)
    return redirect('/user/home/')
def store_Quickcontact(request):
    email    = request.POST['email']
    message  = request.POST['message']
    Quickcontact.objects.create(email=email,message=message)
    return redirect('/user/home/')

# add post 
def add_post(request):
    categories=Category.objects.all()
    context = {'categories':categories}
    return render(request,'user/add_post.html',context)

def store_post(request):
    post_description = request.POST['post_description']
    category   = request.POST['category']
    myfile=request.FILES['f']
    mylocation=os.path.join(settings.MEDIA_ROOT,'post')
    obj= FileSystemStorage(location=mylocation)
    id =  request.user.id
    profile= Profile.objects.get(user_id=id)
    Post.objects.create(post_description=post_description,category_id=category,file_name=myfile.name,user_id=id,area_id=profile.area_id)
    obj.save(myfile.name,myfile)
    return redirect('/user/profile/')
def view_post(request):
    id =  request.user.id
    profile= Profile.objects.get(user_id=id)
    posts = Post.objects.filter(area_id=profile.area_id)
    arr = {}
    # posts = Post.objects.all()
    for i in posts:
        like    = Likes.objects.filter(post_id=i.id, user_like=True).count()
        dislike = Likes.objects.filter(post_id=i.id, user_dislike=True).count()
        arr.update({i:[like, dislike]})

    context={'posts':posts,'arr':arr}
    return render(request,'user/view_post.html',context)
def store_report(request,id):
    posts = Post.objects.all()
    Report.objects.create(post_id=id)
    context={'posts':posts}
    return render(request,'user/view_post.html',context)

def post_details(request,id):  
    result=Post.objects.get(pk=id)
    id=request.user.id
    user=User.objects.get(pk=id)
    com = Comment.objects.filter(post_id=result.id)
    total = Comment.objects.filter(post_id=result.id).count()
    context = {'result':result,'user':user,'com':com,'total':total}
    return render(request,'user/post_details.html',context) 
    context = {'com':com}
    return render(request,'user/post_details.html',context)

def store_comment(request,id):
    msg     = request.POST['msg']
    post_id = id
    user_id =request.user.id

    Comment.objects.create(msg=msg,user_id=user_id,post_id=post_id)
    myurl = '/user/post_details/'+str(post_id)
    return redirect(myurl)

def show_profile(request,id):
    result= User.objects.get(pk=id)
    context = {'result':result}
    return render(request,'user/show_profile.html',context)

def profile(request):
    id=request.user.id
    user=User.objects.get(pk=id)
    posts=Post.objects.filter(user_id=user.id)
    context={'posts':posts}
    return render(request,'user/profile.html',context)

def delete_post(request,id):
    result=Post.objects.get(pk=id)
    result.delete()
    return redirect('/user/profile/')

def add_like(request):
    post_id = request.GET['p_id']
    id = request.user.id

    print(post_id)
    print(id)

    result = Likes.objects.filter(user_id = id, post_id=post_id)
    if result.exists():
        print(1)
        if result[0].user_like == 0 :
            likes = 1
          
        else: 
            print(2)
            likes = 0
        Likes.objects.update_or_create(pk=result[0].id,defaults={'user_like':likes})
        return HttpResponse(0)

    else:
        print(3)
        Likes.objects.create(user_like=1,user_dislike=0,post_id=post_id,user_id=id)
        return HttpResponse(1)


def dis_like(request):
    post_id = request.GET['p_id']
    id = request.user.id

    print(post_id)
    print(id)

    result = Likes.objects.filter(user_id = id, post_id=post_id)
    if result.exists():
        if result[0].user_dislike == 0 :
            dislike = 1
            like = 0
        else: 
            dislike = 0
            like = result[0].user_like
        Likes.objects.update_or_create(pk=result[0].id,defaults={'user_dislike':dislike,'user_like':like})
        return HttpResponse(0)

    else:
        Likes.objects.create(user_like=0,user_dislike=1,post_id=post_id,user_id=id)
        return HttpResponse(1)


def change_password(request):
    context = {}
    return render(request, 'user/change_password.html', context)

def change_password_update(request):
    username = request.user.username
    old_password  = request.POST['old_password']
    new_password  = request.POST['new_password']
    rnew_password = request.POST['rnew_password']

    if new_password == rnew_password:
        user = auth.authenticate(username=username, password=old_password)
        if user is not None:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password Updated Successfully')
            return redirect('/user/home/')
        else:
            messages.success(request, 'Invalid Password Try Again')
            return redirect('/user/change_password/')     
    else:
         messages.success(request, 'Miss Match Password')