from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Documents
from .serializers import DocumentSerializer
from users.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .utils import extract_text_from_pdf, classify_text,summarize_text
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_employees(request):
    return render(request, 'dashboards/dashboard_employees.html')

@login_required
def upload_file(request):
    user_id = request.user.id
    print(f"Logged-in user ID: {user_id}")
    if request.method == 'POST':
        title = request.POST.get('title')
        document_pdf = request.FILES.get('document_pdf')

        if title and document_pdf:
            # Retrieve the logged-in user's ID
            user_id = request.user.id
            print(f"Logged-in user ID: {user_id}")  # Optional debug print

            # Create a new document instance
            new_document = Documents(
                title=title,
                document_pdf=document_pdf,
                status=summarize_text(extract_text_from_pdf(document_pdf)),
                category=classify_text(extract_text_from_pdf(document_pdf)),
                created_by=request.user,  # Set the logged-in user as the creator
            )
            new_document.save()  # Save to the database

            # Prepare the JSON response
            response_data = {
                'title': new_document.title,
                'document_pdf_url': new_document.document_pdf.url,
                'status': new_document.status,
                'category': new_document.category,
                'created_by': user_id,  # Include user ID in the response
            }
            return JsonResponse(response_data)

        # Handle invalid form data
        return JsonResponse({'error': 'Invalid form data'}, status=400)

    return render(request, 'dashboards/dashboard_employees.html')



def admin_dashboard(request):
    users = User.objects.all()
    documents = Documents.objects.all().order_by('-id')[:10]  # Get the 10 most recent documents
    context = {
        'users': users,
        'documents': documents,
    }
    return render(request, 'admin_dashboard.html', context)

@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return JsonResponse({'success': True})


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.role = request.POST.get('role', user.role)
        user.save()
        return redirect('admin_dashboard')
    return render(request, 'edit_user.html', {'user': user})


def manager_dashboard(request):
    # Assuming the manager's ID is stored in the session
    documents = Documents.objects.filter(category='remote_work')
    context = {
        'documents': documents,
        
        
    }
    return render(request, 'manager_dashboard.html', context)

def Financedash(request):
    # Assuming the manager's ID is stored in the session
    
    documents = Documents.objects.filter(category='invoice')
    context = {
        'documents': documents,
        
        
    }
    return render(request, 'Financedash.html', context)

def itdash(request):
    # Assuming the manager's ID is stored in the session
    
    documents = Documents.objects.filter(category='project progress')
    context = {
        'documents': documents,
        
        
    }
    return render(request, 'itdash.html', context)


@require_http_methods(["DELETE"])
def delete_document(request, document_id):
    document = get_object_or_404(Documents, id=document_id)
    if document.managerId == request.session.get('user_id') or request.user.is_superuser:
        document.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Unauthorized'})

def edit_document(request, document_id):
    document = get_object_or_404(Documents, id=document_id)
    if document.managerId != request.session.get('user_id') and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Unauthorized'})
    
    if request.method == 'POST':
        document.title = request.POST.get('title', document.title)
        document.category = request.POST.get('category', document.category)
        document.status = request.POST.get('status', document.status)
        document.save()

        if request.user.is_superuser:
         return redirect('admin_dashboard')

        if document.managerId == request.session.get('user_id') :
          if request.user.role == "Finance Manager" :
           return redirect('Financedash')
          if request.user.role == "IT Manager" :
           return redirect('itdash')     
          if request.user.role == "HR Manager" :
           return redirect('dashboard_employees')
     
        
    return render(request, 'edit_document.html', {'document': document})


@require_http_methods(["POST"])
def approve_document(request, document_id):
    try:
        # Fetch the document using the `document_id` from the URL
        document = get_object_or_404(Documents, id=document_id)
        
        # Check and update the `isApprouved` field
        if document.isApprouved is None:
            document.isApprouved = True  # Set the field to 'Approved'
            document.save()
            return JsonResponse({'success': True, 'message': 'Document approved successfully.'})
        else:
            return JsonResponse({'success': False, 'error': 'Document is already approved or rejected.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_http_methods(["POST"])
def reject_document(request, document_id):
    try:
        # Fetch the document using the `document_id` from the URL
        document = get_object_or_404(Documents, id=document_id)
        
        # Check and update the `isApprouved` field
        if document.isApprouved is None:
            document.isApprouved = False  # Or "Rejected" depending on your field setup
            document.save()
            return JsonResponse({'success': True, 'message': 'Document rejected successfully.'})
        else:
            return JsonResponse({'success': False, 'error': 'Document is already approved or rejected.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def employee_dashboard(request):
    employee_id = request.session.get('user_id')
    documents = Documents.objects.filter(created_by=employee_id).order_by('-id')
    context = {
        'documents': documents,
    }
    return render(request, 'employee_dashboard.html', context)