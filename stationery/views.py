from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def custom_login(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if role == "admin" and not user.is_staff:
                error = "This account is not an Admin account."
            elif role == "user" and user.is_staff:
                error = "Please select Admin for this account."
            else:
                login(request, user)

                if user.is_staff:
                    return redirect("/admin/")
                else:
                    return redirect("/")

        else:
            error = "Invalid username or password."

    return render(request, "registration/login.html", {"error": error})