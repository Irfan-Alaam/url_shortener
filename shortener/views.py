from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from django.contrib import messages
from .selectors import get_user_urls, get_user_url_by_id,get_active_short_url,short_url_exists_for_user
from .services import create_short_url, delete_short_url,increment_click_count,update_short_url

@login_required
@require_POST
def create_url(request):
    originalUrl = request.POST.get("originalUrl")

    if not originalUrl:
        messages.error(request,"originalUrl is required")
    elif short_url_exists_for_user(request.user,originalUrl):
        messages.error(request,f"Short url already exists for the given Original url: {originalUrl}")
    else:
        short_url = create_short_url(
            user=request.user,
            originalUrl=originalUrl
        )
        messages.success(request,f"Short Url created successfully,{short_url}")

    return JsonResponse({
        "id": short_url.id,
        "originalUrl": short_url.originalUrl,
        "shortKey": short_url.shortKey,
        "clickCount": short_url.clickCount,
        "createdAt": short_url.createdAt,
    })

@login_required
def list_urls(request):
    urls = get_user_urls(request.user)
    data = [{
        "id":u.id,
        "originalUrl":u.originalUrl,
        "shortKey":u.shortKey,
        "clickCount":u.clickCount,
        "createdAt":u.createdAt,
        }for u in urls]

    return JsonResponse({"results": data})

@login_required
@require_POST
def delete_url(request, url_id: int):
    short_url = get_user_url_by_id(request.user, url_id)
    delete_short_url(short_url)
    return JsonResponse({"status": "deleted"})


def redirect_short_url(request, short_key: str):
    short_url = get_active_short_url(short_key)
    increment_click_count(short_url)
    return HttpResponseRedirect(short_url.originalUrl)

@login_required
def create_url_view(request):
    short_url = None
    if request.method == "POST":
        originalUrl = request.POST.get("originalUrl")

        if not originalUrl:
            messages.error(request, "Original URL is required.")
        elif short_url_exists_for_user(request.user, originalUrl):
            messages.error(request, f"A short URL already exists for {originalUrl}")
        else:
            short_url = create_short_url(user=request.user, originalUrl=originalUrl)
            messages.success(request, f"Short URL created successfully!")

    return render(request, 'shortener/create_url.html', {'short_url': short_url})

@login_required
def list_urls_view(request):
    urls = get_user_urls(request.user)
    return render(request, 'shortener/url_list.html', {'urls': urls})

@login_required
def delete_url_view(request, url_id):
    if request.method == "POST":
        url = get_user_url_by_id(request.user, url_id)
        delete_short_url(url)
    return redirect('list-urls')

@login_required
def edit_url_view(request, url_id):
    short_url = get_user_url_by_id(request.user, url_id)

    if request.method == "POST":
        originalUrl = request.POST.get("originalUrl")

        if originalUrl:
            update_short_url(
                short_url=short_url,
                originalUrl=originalUrl
            )
            messages.success(request,f"URL updated successfully to: {originalUrl}")
            return redirect("list-urls")
        else:
            messages.error(request,"Orginal Url cannot be empty")
            return redirect("edit-url",url_id=url_id)

    return render(
        request,
        "shortener/edit_url.html",
        {"short_url": short_url}
    )


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list-urls')
    else:
        form = UserCreationForm()
    return render(request, 'shortener/signup.html', {'form': form})

def login_view(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("list-urls")
        else:
            messages.error(request,"Invalid credentials!!! PLEASE CHECK")
    return render(request,'shortener/login.html')
