from django import forms
from django.contrib.auth import get_user_model
from split.models import Expense
User = get_user_model()

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class CreateGroupForm(forms.Form):

    name = forms.CharField(
        max_length=200,
        label="Group name",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Goa Trip 2025'})
    )
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Members"
    )

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)
        if current_user:
            self.fields["members"].queryset = User.objects.exclude(
                id=current_user.id
            )
            
class AddExpenseForm(forms.Form):
    description = forms.CharField(
        max_length=255,
        label="Description"
    )

    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Total Amount"
    )

    paid_by = forms.ModelChoiceField(
        queryset=User.objects.none(),
        label="Paid by"
    )

    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label="Participants"
    )

    split_type = forms.ChoiceField(
        choices=Expense.SplitType.choices,
        label="Split type"
    )

    metadata = forms.CharField(
        required=False,
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        group = kwargs.pop("group")
        super().__init__(*args, **kwargs)

        # Limit users to group members only
        self.fields["paid_by"].queryset = group.members.all()
        self.fields["participants"].queryset = group.members.all()


class SettleExpenseForm(forms.Form):
    paid_by = forms.ModelChoiceField(queryset=User.objects.all())
    paid_to = forms.ModelChoiceField(queryset=User.objects.all())
    amount = forms.DecimalField(max_digits=10, decimal_places=2)