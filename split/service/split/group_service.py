from split.models import Group, Expense

from django.contrib.auth import get_user_model

from .expense_service import ExpenseService
from .balance_service import BalanceService

User=get_user_model()

class UserNotFound (Exception):
    pass
class GroupNotFound (Exception):
    pass
class UserAlreadyMember(Exception):
    pass
class GroupService:

  
    def create_group(self,name,creator,members):
        group=Group.objects.create(name=name)
        group.members.add(creator)
        for user in members:
            group.members.add(user)

        return group
        


    def add_members(self,group_id,user_id):

        try:
            group=Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            raise GroupNotFound("GroupNotFound")
        try:
            user=User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise UserNotFound("UserNotFound")
        if group.members.filter(id=user.id).exists():
            raise UserAlreadyMember("user already in the group")
        group.members.add(user)
        return group

        

    def add_expense(
            self,
            group_id,
            description,
            amount,
            paid_by,
            participants,
            split_type,
            meta_data=None
    ):
        try:
            group=Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            raise GroupNotFound(" Group Not Found")
        
        # The 'paid_by' from the form is a User object. We need to use its ID for the filter.
        if not group.members.filter(id=paid_by.id).exists():
            raise ValueError("Payer is not a group member")

        # The 'participants' from the form is already a queryset of User objects.
        for user in participants:
            if not group.members.filter(id=user.id).exists():
                raise ValueError(f"{user} not in group")
            
        expense=ExpenseService().add_expense(
            group=group,
            description=description,
            amount=amount,
            paid_by=paid_by,
            participants=participants,
            split_type=split_type,
            metadata=meta_data,
        )
        return expense

    def record_settlement(self, group_id, paid_by, paid_to, amount):
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            raise GroupNotFound("Group not found")

        # A settlement is just an expense where the payer pays the full amount to the payee
        return ExpenseService().add_expense(
            group=group,
            description="Settlement",
            amount=amount,
            paid_by=paid_by,
            participants=[paid_to],
            split_type=Expense.SplitType.EQUAL,
            is_settlement=True
        )


    def settle_balances(self,group_id):
        try:
            group=Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            raise ValueError("Group does not found")
        return  BalanceService().settle_group_balances(group)

    def group_balances(self,group_id):
        try:
            group=Group.objects.get(id=group_id)

        except Group.DoesNotExist:
            raise GroupNotFound("Group not Found")
        return BalanceService().compute_group_balances(group)


    def user_balance(self,group_id,user_id):
        try:
            group = Group.objects.get(id=group_id)


        except Group.DoesNotExist:
            raise GroupNotFound("Group not found")
        try:

            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise UserNotFound("User not found")
        
        if not group.members.filter(id=user.id).exists():
            raise ValueError("User is not a member of this group")
        return BalanceService().get_user_balance(group, user)