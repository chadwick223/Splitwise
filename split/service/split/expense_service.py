
from decimal import Decimal,ROUND_HALF_UP
from split.models import Expense, Split
from django.db import transaction
from .split_strategies.equal import EqualSplitStrategy
from .split_strategies.percentage import PercentageSplitStrategy
from .split_strategies.exact import ExactSplitStrategy

class ExpenseService:
    

    def add_expense(
            self,
            group,
            description,
            amount,
            paid_by,
            participants,
            split_type,
            metadata=None,
            is_settlement=False
    ):
        total_amount=Decimal(str(amount))
        STRATEGY_MAP={
            Expense.SplitType.EQUAL :EqualSplitStrategy(),
            Expense.SplitType.PERCENTAGE :PercentageSplitStrategy(),
            Expense.SplitType.EXACT :ExactSplitStrategy(),

        }
        strategy=STRATEGY_MAP.get(split_type)

        if not strategy:
            raise ValueError("Invalid split type")


        with transaction.atomic():

            expense=Expense.objects.create(
                group=group,
                description=description,
                amount=amount,
                paid_by=paid_by,
                split_type=split_type,
                is_settlement=is_settlement

            )
            shares=strategy.split(total_amount,participants,metadata)
            splits=[
                Split(
                    expense=expense,
                    user=user,
                    amount=share_amount,
                )
                for user,share_amount in shares.items()
            ]
            Split.objects.bulk_create(splits)



            return expense
