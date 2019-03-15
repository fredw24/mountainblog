from django.shortcuts import render, redirect
from .models import User, Mountain, Blog
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, 'ski/index.html')

def createUser(request):

    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect('/')
    
    else:
        first = request.POST['fname']
        last = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pcode']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        print(pw_hash) 

        newuser = User.objects.create(first_name = first, last_name = last, email = email, password = pw_hash.decode())
        request.session['key'] = newuser.email        
        email = User.objects.get(email = request.POST['email'])
        request.session['fname'] = newuser.first_name
        request.session['id'] = newuser.id
        request.session['lname'] = newuser.last_name

        return redirect('/success')

def login(request):

    if request.method == "GET":
        return redirect('/')
    else:

        errors = User.objects.login_validator(request.POST)


        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)

            return redirect('/')

        else:
            email = User.objects.get(email = request.POST['email'])
            request.session['key'] = email.email
            request.session['fname'] = email.first_name
            request.session['id'] = email.id
            request.session['lname'] = email.last_name 
            return redirect("/success")

def success(request):

    context ={
        'oneuser' : request.session['key'],
        'firstname': request.session['fname'],
        'lastname': request.session['lname'],
        'id': request.session['id'],
        'all_Mountain': Mountain.objects.all()
    }

    return render(request, "ski/list.html", context)

def create(request):

    context = {

        'id': request.session['id']
    }

    return render(request, "ski/new.html", context)

def createprocess(request):

    errors = Mountain.objects.mountain_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        context = {
            'mountID' : request.POST['montID'],
            'id': request.POST['userID']
        }

        return redirect('/newMountain', context)

    else:

        title = request.POST['newmountain']
        location = request.POST['newlocation']
        userid = request.POST['userid']
        currentuser = User.objects.get(id = int(userid))

        Mountain.objects.create(mountain = title, location = location, user = currentuser)

        return redirect('/success')

def blogs(request):
    mountid = request.POST['mountainid']
    context = {
        'mountID' : mountid,
        'id': request.session['id']
    }

    return render(request, "ski/blog.html", context)

def blogprocess(request):

    errors = Blog.objects.blog_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        context = {
        'mountID' : request.POST['montID'],
        'id': request.session['id']
        }

        return render(request, "ski/blog.html", context)

    else:

        userID = request.POST['userID']
        montID = request.POST['montID']
        blog = request.POST['blogprocess']

        getuser = User.objects.get(id = int(userID))
        getmont = Mountain.objects.get(id = int(montID))

        Blog.objects.create(blog = blog, user = getuser, mountain = getmont)


        return redirect('/success')

def blogedit(request):

    getblog = Blog.objects.get(id = int(request.POST['blogid']))

    context = {
        'blog': getblog.blog,
        'id': getblog.id
    }

    return render(request, 'ski/editblog.html', context)

def blogeditprocess(request):

    errors = Blog.objects.blog_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        getblog = Blog.objects.get(id = int(request.POST['blogid']))

        context = {
        'id': getblog.id,
        'blog' : getblog.blog
        }

        return render(request, "ski/editblog.html", context)
    else:

        getblog = Blog.objects.get(id = int(request.POST['blogid']))

        getblog.blog = request.POST['blogprocess']
        getblog.save()

        return redirect('/success')

def deleteblog(request):

    removeblog = Blog.objects.get(id = int(request.POST['blogidremove']))
    removeblog.delete()
    return redirect('/success')


def viewing(request):

    certainmountain = Mountain.objects.get(id = int(request.POST['mountainid']))

    context ={

        'mount': certainmountain,
        'mountblog' : Blog.objects.filter(mountain_id = int(request.POST['mountainid'])),
        'id' : request.session['id'],
        'like': certainmountain.users_who_like.count()
        
    }

    return render(request, 'ski/view.html', context)

def like(request):

    errors = Mountain.objects.like_validator(request.POST)

    if len(errors) > 0:

        for key, value in errors.items():
            messages.error(request, value)

    else:
        getMount = Mountain.objects.get(id = int(request.POST['mountainid']))
        getUser = User.objects.get(id = int(request.POST['userid']))

        getMount.users_who_like.add(getUser)

    return redirect('/success')

def unlike(request):

    errors = Mountain.objects.unlike_validator(request.POST)

    if len(errors) > 0:
        print('error')
        for key, value in errors.items():
            messages.error(request, value)

    else:
        print('check')
        getMount = Mountain.objects.get(id = int(request.POST['mountainid']))
        getUser = User.objects.get(id = int(request.POST['userid']))

        getMount.users_who_like.remove(getUser)

    return redirect('/success')



def back(request):

    return redirect('/success')

def logout(request):
    if 'key' in request.session:

        del request.session['key'] 

    return redirect('/')