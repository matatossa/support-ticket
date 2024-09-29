# support/views.py
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import  ClaimForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Claim, Customer, User

@login_required
def claimpage(request):
    return render(request, 'claimpage.html')

def is_admin(user):
    return user.role == 'admin'

@user_passes_test(is_admin)
def adminside(request):
    claims = Claim.objects.all()
    return render(request, 'support/adminside.html', {'claims': claims})

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .forms import ClaimForm
from .models import Claim

@login_required
def clientside(request):
  
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.client = request.user
            claim.save()
            return redirect('support:clientside')
    else:
        form = ClaimForm()

   
    user_claims = Claim.objects.filter(client=request.user)
    return render(request, 'supportclaim/clientside.html', {'claims': user_claims, 'form': form})

@user_passes_test(lambda user: user.role == 'admin')
@login_required
def adminside(request):
    all_claims = Claim.objects.all()
    return render(request, 'supportclaim/adminside.html', {'claims': all_claims})

@login_required
@user_passes_test(lambda user: user.role == 'admin')
def update_claim_status(request, claim_id):
    claim = Claim.objects.get(id=claim_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Claim.STATUS_CHOICES):
            claim.status = new_status
            claim.save()
        return redirect('support:adminside')

    return render(request, 'supportclaim/update_claim_status.html', {'claim': claim})
# Admin Side View
@login_required
def adminside(request):
    all_claims = Claim.objects.all()
    return render(request, 'supportclaim/adminside.html', {'claims': all_claims})
@login_required
def submit_claim(request):
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.client = request.user
            claim.save()
            return redirect('support:claimpage')
    else:
        form = ClaimForm()
    
    return render(request, 'supportclaim/submit_claim.html', {'form': form})
@login_required
@user_passes_test(lambda user: user.role == 'admin')
def delete_claim(request, claim_id):
    claim = Claim.objects.get(id=claim_id)
    if request.method == 'POST':
        claim.delete()
        return redirect('support:adminside')
from django.shortcuts import redirect
from .models import Claim, ArchivedClaim

@login_required
def confirm_claim(request, claim_id):
    try:
       
        claim = Claim.objects.get(id=claim_id, client=request.user)

      
        if claim.status == 'solved':
            # Crer claim archhive
            ArchivedClaim.objects.create(
                client=claim.client,
                title=claim.title,
                website_link=claim.website_link,
                description=claim.description,
                created_at=claim.created_at,
            )
           
            claim.delete()

            return redirect('support:clientside')
        else:
            return HttpResponse("Invalid claim status")
    except Claim.DoesNotExist:
        return HttpResponse("Claim does not exist")

@login_required
def reject_claim(request, claim_id):
    claim = Claim.objects.get(id=claim_id)  
    if request.method == 'POST' and claim.status == 'solved':
        claim.status = 'in_progress'  
        claim.save()  
    return redirect('support:clientside')  

@login_required
@user_passes_test(lambda user: user.role == 'admin')
def archived_claims_list(request):
    archived_claims = ArchivedClaim.objects.all()
    return render(request, 'supportclaim/archived_claims.html', {'archived_claims': archived_claims})

def list_of_problems_view(request):
    archived_claims = ArchivedClaim.objects.all() 
    return render(request, 'supportclaim/problems_list.html', {'archived_claims': archived_claims})


@login_required
@user_passes_test(lambda user: user.role == 'admin')
def delete_archived_claim(request, archived_claim_id):
    archived_claim = ArchivedClaim.objects.get(id=archived_claim_id)
    if request.method == 'POST':
        archived_claim.delete()
        return redirect('support:archived_claims_list')
@login_required
@user_passes_test(lambda user: user.role == 'admin')
def update_cause(request, archived_claim_id):
    try:
        archived_claim = ArchivedClaim.objects.get(id=archived_claim_id)
    except ArchivedClaim.DoesNotExist:
        return redirect('support:problems_list') 

    if request.method == 'POST':
        cause = request.POST.get('cause')
        archived_claim.cause = cause
        archived_claim.save()
        return redirect('support:problems_list') 

    return render(request, 'supportclaim/problems_list.html', {'archived_claim': archived_claim})
def about(request):
    return render(request,"about.html")

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404


@login_required
@user_passes_test(lambda user: user.role == 'admin')
def manage_users(request):
    users = get_user_model().objects.all()  
    return render(request, 'supportclaim/manage_users.html', {'users': users})

# Update user role
@login_required
@user_passes_test(lambda user: user.role == 'admin')
def update_user_role(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    if request.method == 'POST':
        new_role = request.POST.get('role')
        if new_role in ['admin', 'client']:  # Assuming these are the roles
            user.role = new_role
            user.save()
        return redirect('support:manage_users')

# Delete user
@login_required
@user_passes_test(lambda user: user.role == 'admin')
def delete_user(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    if request.method == 'POST':
        user.delete()
    return redirect('support:manage_users')
from django.shortcuts import render

def about1(request):
    return render(request, 'about1.html')

