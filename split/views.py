from django.shortcuts import render,redirect,get_object_or_404
from split.models import Group
import json
from .forms import CreateGroupForm, SignupForm
from split.forms import AddExpenseForm, SettleExpenseForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from split.service.split.group_service import GroupService
from django.contrib.auth.decorators import login_required
from split.service.split.balance_service import BalanceService

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    groups = Group.objects.filter(members=request.user)
    return render(request, "split/home.html", {"groups": groups})
@login_required
def create_group(request):

    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            GroupService().create_group(
                name=form.cleaned_data["name"],
                creator=request.user,
                members=form.cleaned_data["members"]
            )
            return redirect("home")
    else:
        form = CreateGroupForm()

    return render(request, "split/create_group.html", {"form": form})

@login_required
def group_detail(request, group_id):

    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return render(request, "404.html", status=404)

    # Optional safety check
    if request.user not in group.members.all():
        return render(request, "403.html", status=403)
    balance_service = BalanceService()
    balances = balance_service.compute_group_balances(group)
    simplified_debts = balance_service.settle_group_balances(group)
    return render(request, "split/group_detail.html", {
        "group": group,
        "members": group.members.all(),
        "balances": balances,
        "settlements": simplified_debts,
    })

@login_required
def add_expense(request, group_id):

    group = get_object_or_404(Group, id=group_id)

    if request.user not in group.members.all():
        return render(request, "403.html", status=403)

    if request.method == "POST":
        form = AddExpenseForm(request.POST, group=group)
        if form.is_valid():
            metadata = form.cleaned_data.get("metadata")

            if metadata:
                metadata = json.loads(metadata)

            GroupService().add_expense(
                group_id=group.id,
                description=form.cleaned_data["description"],
                amount=form.cleaned_data["amount"],
                paid_by=form.cleaned_data["paid_by"],
                
                participants=form.cleaned_data["participants"],
                split_type=form.cleaned_data["split_type"],
                meta_data=metadata
            )
            return redirect("group_detail", group_id=group.id)
    else:
        form = AddExpenseForm(group=group)

    return render(request, "split/add_expense.html", {
        "group": group,
        "form": form
    })

@login_required
def settle_expense(request, group_id):
    if request.method == "POST":
        group = get_object_or_404(Group, id=group_id)
        
        if request.user not in group.members.all():
            return render(request, "403.html", status=403)

        form = SettleExpenseForm(request.POST)
        if form.is_valid():
            GroupService().record_settlement(
                group_id=group.id,
                paid_by=form.cleaned_data["paid_by"],
                paid_to=form.cleaned_data["paid_to"],
                amount=form.cleaned_data["amount"]
            )
        
        return redirect("group_detail", group_id=group.id)
    
    return redirect("home")

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "split/signup.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "split/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")
