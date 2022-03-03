import httpx
from asgiref.sync import sync_to_async

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User


def get_local_users():
    return list(User.objects.all())

def filter_local_users(id):
    return User.objects.filter(id=id)

async def index(request):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/users/users/", auth=("admin", "password")
        )
    json = response.json()
    remote_users = json["results"]
    local_users = await sync_to_async(get_local_users, thread_sensitive=True)()
    return render(
        request,
        "users/index.html",
        {"remote_users": remote_users, "local_users": local_users},
    )
    
async def remote_user_view(request, id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/users/users/{id}/", auth=('admin', 'password'))
        user = response.json()
    return render(request, 'users/user_view.html', {'user': user})

def local_user_view(request, pk):
    user = User.objects.get(pk=pk)
    return render(request, 'users/user_view.html', {'user': user})

# async def user_view(request, id):
#     async with httpx.AsyncClient() as client:
#         response = await client.get(f"http://localhost:8000/users/users/{id}/", auth=('admin', 'password'))
#         user = response.json()

#     user = await sync_to_async(filter_local_users, thread_sensitive=True)(user['id'])
#     return render(request, 'users/user_view.html', {'user': user})

async def dogs_view(request):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/users/dogs/", auth=("admin", "password")
        )
    json = response.json()
    dogs = json["results"]
    return render(
        request,
        "users/dogs_view.html",
        {"dogs": dogs},
    )