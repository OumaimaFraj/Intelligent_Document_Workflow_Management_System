from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .serializers import UserRegistrationSerializer, LoginSerializer, TokenSerializer


from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate

from django.http import HttpResponseRedirect
from django.urls import reverse

User = get_user_model()


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        # Traitement de l'inscription
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Récupérer le rôle et la langue depuis les données de la requête ou définir des valeurs par défaut
            role = request.data.get('role', 'employee')
            language = request.data.get('language', 'English')
            user.role = role
            user.language = language
            user.save()
            return redirect('login')  
    return render(request, 'myapp/registre.html')
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            if user.role == 'Employee':
                return redirect(reverse('dashboard_employees'))
            elif user.role == 'admin':
                return redirect(reverse('admin_dashboard'))
            elif user.role == 'HR Manager':
                return redirect(reverse('manager_dashboard'))
            elif user.role == 'Finance Manager':
                return redirect(reverse('Financedash'))
            elif user.role == 'IT Manager':
                return redirect(reverse('itdash'))
        else:
            error_message = 'Invalid email or password.'
            return render(request, 'myapp/login.html', {'error_message': error_message})
    
    return render(request, 'myapp/login.html')