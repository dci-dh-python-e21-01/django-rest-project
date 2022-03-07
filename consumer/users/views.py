import httpx
from asgiref.sync import sync_to_async
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import DogForm, UserForm

def get_local_users():
    return list(User.objects.all())

# def filter_local_users(id):
#     return User.objects.filter(id=id)

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


#to be finished 
async def add_user(request):
    if request.method == "POST":
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://localhost:8000/users/users/",
                auth=("admin", "password"),
                data=request.POST
            )
            print(response)
        return redirect("/users")

    return render(request, "users/add_user.html", {"user_form": UserForm()})

async def delete_user(request, id):
    if request.method == "POST":
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"http://localhost:8000/users/users/{id}/",
                auth=("admin", "password")
            )
        return redirect("/users")

    return render(request, "users/delete_user.html")

#to be finished 
async def edit_user(request, id):
    if request.method == "POST":
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"http://localhost:8000/users/users/{id}/",
                auth=("admin", "password"),
                data=request.POST
            )
        return redirect(f"/users/users/{id}/")

    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/users/users/{id}/", auth=("admin", "password"))
    user = response.json()
    
    return render(request, "users/edit_user.html", { "user": UserForm(initial={
        "id": user["id"],
        "url": user["url"],
        "username": user["username"],
        "email": user["email"],
        "groups": user["groups"],
    }) })

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
async def dogs_detail(request, id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://127.0.0.1:8000/users/dogs/{id}/", auth=('admin', 'password'))
    dog = response.json()
    return render(request, 'users/dog_view.html', {'dog': dog})

async def add_dog(request):
    if request.method == "POST":
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://localhost:8000/users/dogs/",
                auth=("admin", "password"),
                data=request.POST
                
            )
        return redirect("/users/dogs")

    return render(request, "users/add_dog.html", { "dog_form": DogForm()})


async def edit_dog(request, id):
    if request.method == "POST":
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"http://localhost:8000/users/dogs/{id}/",
                auth=("admin", "password"),
                data=request.POST
            )
        return redirect(f"/users/dogs/{id}")

    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/users/dogs/{id}/", auth=("admin", "password"))
    dog = response.json()
    
    return render(request, "users/edit_dog.html", { "dog": DogForm(initial={
        "id": dog["id"],
        "name": dog["name"],
        "breed": dog["breed"],
        "age": dog["age"],
        "is_friendly": dog["is_friendly"],
    }) })

async def delete_dog(request, id):
    if request.method == "POST":
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"http://localhost:8000/users/dogs/{id}/",
                auth=("admin", "password")
            )
        return redirect("/users/dogs")

    return render(request, "users/delete_dog.html")

