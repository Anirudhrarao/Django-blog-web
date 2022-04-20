from django.conf import settings
from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
from home.models import Contact
from django.contrib import messages 
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def home(request):
    allpost = Post.objects.all()
    context = {'allpost':allpost}
    return render(request, 'home/home.html',context)
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        contents = request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or  len(contents)<4:
            messages.error(request, 'Please fill the form correctly')
        else:
            contact_details = Contact(name=name, email=email, phone=phone, content=contents)
            contact_details.save()
        messages.success(request, 'Your message has been successfully sent')     
    return render(request, 'home/contact.html')
def about(request):
    return render(request, 'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query) > 78:
        allpost = Post.objects.none()
    else:
        allposttitle = Post.objects.filter(title__icontains=query)
        # allpostcontents = Post.objects.filter(content__icontains=query)
        allpostauthor = Post.objects.filter(author__icontains=query)
        allpost =allposttitle.union(allpostauthor)
    if allpost.count() == 0:
        messages.warning(request, 'No search result found')

    context = {'allpost':allpost,
                'query':query}
    return render(request,"home/search.html",context)


def handleSignup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        SpecialSym =['$', '@', '#', '%']
        if len(username) > 10:
            messages.error(request,"Username must be under 10 characters.")
            return redirect('home')
        if not username.isalnum():
            messages.error(request,"Username should only contains alphabets and numbers.")
        if password != cpassword:
            messages.error(request,"Password not matched.")
            return redirect('home')
        if len(password) < 8:
            messages.error(request,"Length password is too short it should be length of 8.")
            return redirect('home')
        if not any(char in SpecialSym for char in password):
            messages.error(request,"Password should contains special symbols like $', '@', '#', '%.")
            return redirect('home')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been succesfully created.")
        return redirect('home')
    else:
        return HttpResponse("404 not found")

def handleLogin(request):
    if request.method == 'POST':
        usernamelog = request.POST['usernamelogin']
        userpasswords = request.POST['passwordlogin']
        user = authenticate(username = usernamelog, password = userpasswords)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again with valid credentials ")
            return redirect('home')
    return HttpResponse('404 not found')
def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')
