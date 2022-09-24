from django.shortcuts import render,HttpResponse,redirect
from blog.models import Post,BlogComments
from django.contrib import messages
from django.contrib.auth.models import User
# from blog.templatetags import extras
# Create your views here.
def bloghome(request):
    allpost = Post.objects.all()
    context = {'allpost':allpost}
    return render(request, 'blog/bloghome.html',context)
def blogpost(request, slug):
    allpost = Post.objects.filter(slug=slug).first()
    comments = BlogComments.objects.filter(post=allpost,parent=None) 
    replies = BlogComments.objects.filter(post=allpost).exclude(parent=None)
    repdict ={}
    for reply in replies:
        if reply.parent.sno not in repdict.keys():
            repdict[reply.parent.sno] = [reply]
        else:
            repdict[reply.parent.sno].append(reply)
    context = {'allpost':allpost,'comment':comments,'user':request.user,'repdict':repdict}
    return render(request, 'blog/blogpost.html', context)

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        postsno = request.POST.get("postsno")
        post = Post.objects.get(sno=postsno)
        parentSno = request.POST.get("parentSno","")
        if parentSno == "":
            comment = BlogComments(comment=comment,user=request.user, post=post)
            comment.save()
            messages.success(request,"Your comment has been posted successfully")
        else:
            parent=BlogComments.objects.get(sno=parentSno)
            comment=BlogComments(comment=comment,user=request.user,post=post, parent=parent)
            comment.save()
            messages.success(request,"Your reply has been posted succesfully")
        
    return redirect(f"/blog/{post.slug}")


    