# split/service/split/balance_service.py

from collections import defaultdict
from decimal import Decimal
from split.models import Split

class BalanceService:

    def compute_group_balances(self, group):

        balances = defaultdict(lambda: Decimal("0.00"))

        splits = Split.objects.filter(expense__group=group).select_related(
            "expense", "user", "expense__paid_by"
        )

        for split in splits:
            payer = split.expense.paid_by
            user = split.user
            amount = split.amount

            balances[payer] += amount
            balances[user] -= amount

        return dict(balances)
    
    def get_user_balance(self,group,user):
        
        balances=self.compute_group_balances(group)
        return balances.get(user,Decimal("0.00"))
        
        
    def settle_group_balances(self,group):
        
        balances=self.compute_group_balances(group)
        
        creditors=[]
        debtors=[]
        for user, balance in balances.items():
            if balance > 0:
                creditors.append([user, balance])
            elif balance < 0:
                debtors.append([user, -balance]) 
        settlements=[]
        
        i=j=0
        while i < len(debtors) and j < len(creditors):
            debtor, debt = debtors[i]
            creditor, credit = creditors[j]

            settled_amount = min(debt, credit)

            settlements.append({
                "from": debtor,
                "to": creditor,
                "amount": settled_amount
            })

            debtors[i][1] -= settled_amount
            creditors[j][1] -= settled_amount

            if debtors[i][1] == 0:
                i += 1
            if creditors[j][1] == 0:
                j += 1

        return settlements
        
