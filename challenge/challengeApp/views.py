from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from .models import User, \
                    AnalyticsAccount, \
                    AnalyticsProperties, \
                    AnalyticsViews, LogEvents
from .api_analytics import AnalyticsApi
from django.contrib import messages
import json
import time
import logging

def get_context(email, password, caller):
    """ Method to retrives informations about Users, Accounts, Properties and Views
        according to 'caller' parameter.
        Args:
            email: user e-mail
            password: user password
            valler: parameter who tells if API should be called or not.
        Returns:
            context: a dictionary with the requested informations
    """
    users = User.objects.filter(email=email,
                                password=password).values()
    if users:
        accounts = ""
        if caller == 'gadata':
            call_api = AnalyticsApi(users[0]["credentials"], users[0]["id"])
            call_api.main()
          
        accounts = AnalyticsAccount.objects.filter(user_id=users[0]["id"]).values()
            
        if accounts:
            properties = AnalyticsProperties.objects.filter(accountid__in= \
                [account["id"] for account in accounts], userid=users[0]["id"]).values()
            if properties:
                views = AnalyticsViews.objects.filter(propid__in= \
                    [prop["id"] for prop in properties], userid=users[0]["id"]).values()
                if views:
                    context = {'user': users[0]["full_name"],
                               'accounts': accounts,
                               'properties': properties,
                               'views': views,
                               'caller': caller,
                               'userid': users[0]["id"]
                    }
                    return context
                else:
                    context = {'user': users[0]["full_name"],
                               'accounts': accounts,
                               'properties': properties,
                               'views': None,
                               'caller': caller,
                                'userid': users[0]["id"]
                    }
                    return context
            else:
                context = {'user': users[0]["full_name"],
                           'accounts': accounts,
                           'properties': None,
                           'views': None,
                           'caller': caller,
                           'userid': users[0]["id"]
                }
                return context
        else:
            context = {'user': users[0]["full_name"],
                       'accounts': None,
                       'properties': None,
                       'views': None,
                       'caller': caller,
                       'userid': users[0]["id"]
            }
            return context
    else:
        return None

def login(request):
    """ Method to log in the user if email and password matches.
        If matches the last account inserted it's loaded to the user.
        Args:
            request: HttpRequest object, which contains data about the request.
        Returns:
            render: render the pages into the browser and returns a 
                    HttpResponse object with that rendered text.
    """
    if request.method == 'POST':        
        login_data = request.POST.dict()
        
        # Save user and password in a django session for later use
        request.session["email"] = login_data.get("email")
        request.session["password"] = login_data.get("password")

        context = get_context(login_data.get("email"), 
                              login_data.get("password"),
                              'login')
        if context:
            request.session["userid"] = context["userid"]
            return render(request, 'gadata/gadata.html', context)
        else:
            messages.error(request, "E-mail ou senha incorretos!") 
            return render(request, 'accounts/login.html')
    else:    
        return render(request, 'accounts/login.html')

def gadata(request):
    """ Method call API from 'home' page.
        Observe when call get_context method, the parameter caller it's 
        defined as 'gadata', this tells to invoke API. 
        Args:
            request: HttpRequest object, which contains data about the request.
        Returns:
            render: render the pages into the browser and returns a 
                    HttpResponse object with that rendered text.
    """
    if request.method == 'POST':
        context = get_context(request.session["email"], 
                              request.session["password"],
                              'gadata')
       
        if context:
            request.session["userid"] = context["userid"]
            return render(request, 'gadata/gadata.html', context)
        else:
            messages.error(request, 'Dados não encontrados')
            return render(request, 'gadata/gadata.html', context)
    else:
        return render(request, 'gadata/gadata.html')

def signup(request):
    """ Method to create and save a new user.
        Args:
            request: HttpRequest object, which contains data about the request.
        Returns:
            render: render the pages into the browser and returns a 
                    HttpResponse object with that rendered text.
            or
            redirect: takes you to the defined page.
    """
    if request.method == 'POST': 
        uploaded_file = request.FILES['document']
        try:
            file_as_json = json.loads(uploaded_file.read())
            account_data = request.POST.dict()

            # Check if e-mail already exists in database
            check_unique = User.objects.filter( \
                email=account_data["email"]).exists()
            if check_unique:
                messages.error(request, "Usuário já cadastrado.")
                return render(request, 'signup/signup.html') 
            else:
                user = User(full_name=account_data["fullname"],
                            gender=account_data["gender"],
                            email=account_data["email"],
                            password=account_data["password"],
                            credentials=file_as_json
                )            
                user.save()
                messages.success(request, "Usuário criado com sucesso!")          
                return redirect('login')
        except:
            messages.error(request, "Arquivo inválido") 
            return render(request, 'signup/signup.html')
    else:    
        return render(request, 'signup/signup.html')

def log(request):
    # Show logs stored in database
    user_logs = LogEvents.objects.filter(userid=request.session["userid"]).values()
    context = {
        'logs': user_logs 
    }    
    return render(request, 'log/log.html', context)

def home(request):
    # Sent user back to 'home' page
    context = get_context(request.session["email"], 
                              request.session["password"],
                              'home')
    if context:
        request.session["userid"] = context["userid"]
        return render(request, 'gadata/gadata.html', context)
    else:
        messages.error(request, 'Dados não encontrados')
        return render(request, 'gadata/gadata.html', context)

def logout(request):
    # Clean session attributes
    request.session["email"] = ""
    request.session["password"] = "" 
    request.session["userid"] = 0
    return render(request, 'accounts/login.html')