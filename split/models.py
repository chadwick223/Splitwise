from django.db import models
from django.conf import settings

class Group(models.Model):
    name=models.CharField(
        max_length=200,
        unique=True,
    )
    members=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='expense_groups')

    def __str__(self):
        return self.name

class Expense(models.Model):

    class SplitType(models.TextChoices):
        EQUAL='EQUAL','Equal'
        PERCENTAGE='PERCENTAGE','Percentage'
        EXACT='EXACT','Exact'
    
    group=models.ForeignKey(Group,on_delete=models.CASCADE,related_name='expenses')
    
    description=models.CharField(max_length=255)
    
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    
    paid_by=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='paid_expenses'
    )

    split_type=models.CharField(
        max_length=20,
        choices=SplitType.choices,
        default=SplitType.EQUAL,
    )
    is_settlement = models.BooleanField(default=False)
    

    def __str__(self):
        if self.is_settlement:
            return f"Settlement: {self.paid_by} paid {self.amount}"
        return f"{self.description} {self.amount}"
    

class Split(models.Model):
    expense=models.ForeignKey(Expense,on_delete=models.CASCADE,related_name="splits")

    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="splits",

    )
    amount=models.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=["expense","user"],
                name="unique_user_expense_split"
            )
        ]

    def __str__(self):
        return f"{self.user} owes {self.amount}"

    

    
