from decimal import Decimal,ROUND_HALF_UP

from .base import SplitStrategy

class EqualSplitStrategy(SplitStrategy):
    def split(self,total_amount,participants,metadata=None):
        num=len(participants)
        if num==0:
            return {}
        
        share_amount= (total_amount/num).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)
        return {user: share_amount for user in participants}
