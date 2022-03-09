import httpx
from asgiref.sync import sync_to_async
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import DogForm, UserForm
from django.conf import settings


def get_local_users():
    return list(User.objects.all())

# def filter_local_users(id):
#     return User.objects.filter(id=id)

async def index(request):
    context = {}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:8000/users/users/",
                headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
            )
        json = response.json()
        context["remote_users"] = json["results"]
    except httpx.RequestError as exc:
        context["connection_error"] = True
    context["local_users"] = await sync_to_async(
        get_local_users, thread_sensitive=True
    )()
    return render(
        request,
        "users/index.html",
        context,
    )
    
async def remote_user_view(request, id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/users/users/{id}/", headers={"Authorization": f"Token {settings.AUTH_TOKEN}"})
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


async def add_user(request):
    context = {"user_form": UserForm()}
    if request.method == "POST":
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"http://localhost:8000/users/users/",
                    headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
                    data=request.POST
                )
            return redirect("/users")
        except httpx.RequestError as exc:
            context["connection_error"] = True

    return render(request, "users/add_user.html", context)

async def delete_user(request, id):
    if request.method == "POST":
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"http://localhost:8000/users/users/{id}/",
                headers={"Authorization": f"Token {settings.AUTH_TOKEN}"}
            )
        return redirect("/users")

    return render(request, "users/delete_user.html")

async def edit_user(request, id):
    if request.method == "POST":
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"http://localhost:8000/users/users/{id}/",
                headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
                data=request.POST
            )
        return redirect(f"/users/users/{id}/")

    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/users/users/{id}/", headers={"Authorization": f"Token {settings.AUTH_TOKEN}"})
    user = response.json()
    
    return render(request, "users/edit_user.html", { "user": UserForm(initial={
        "id": user["id"],
        "url": user["url"],
        "username": user["username"],
        "email": user["email"],
        
    }) })

async def dogs_view(request):
    context = {}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
            "http://localhost:8000/users/dogs/", headers={"Authorization": f"Token {settings.AUTH_TOKEN}"}
        )
        json = response.json()
        context["dogs"] = json["results"]
    except httpx.RequestError as exc:
        context["connection_error"] = True
    return render(
        request,
        "users/dogs_view.html",
        context,
    )
async def dogs_detail(request, id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://127.0.0.1:8000/users/dogs/{id}/", headers={"Authorization": f"Token {settings.AUTH_TOKEN}"})
    dog = response.json()
    return render(request, 'users/dog_view.html', {'dog': dog})

async def add_dog(request):
    context = {"dog_form": DogForm()}
    if request.method == "POST":
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"http://localhost:8000/users/dogs/",
                    headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
                    data=request.POST
            )
            return redirect("/users/dogs")
        except httpx.RequestError as exc:
            context["connection_error"] = True
    return render(request, "users/add_dog.html", context)


async def edit_dog(request, id):
    if request.method == "POST":
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"http://localhost:8000/users/dogs/{id}/",
                headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
                data=request.POST
            )
        return redirect(f"/users/dogs/{id}")

    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/users/dogs/{id}/", headers={"Authorization": f"Token {settings.AUTH_TOKEN}"})
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
                headers={"Authorization": f"Token {settings.AUTH_TOKEN}"}
            )
        return redirect("/users/dogs")

    return render(request, "users/delete_dog.html")

