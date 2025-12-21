from decimal import Decimal,ROUND_HALF_UP

from .base import SplitStrategy

class PercentageSplitStrategy(SplitStrategy):
    def split(self,total_amount,participants,metadata=None):
        if not metadata:
            raise ValueError("Percentage data is required in metadeta")
        # 1. Validate total percentage equals 100
        total_percentage = sum(Decimal(str(p)) for p in metadata.values())

        


        if total_percentage !=Decimal("100"):
            raise ValueError(f"Total percentage must be 100, got {total_percentage}")



        shares={}
        comulative_sum=Decimal("0.00")
        participant_list=list(participants)
        for i,user in enumerate(participant_list):

            if str(user.id) not in metadata:
                raise ValueError(f"Missing percentage for user")
            
            percentage=Decimal(str(metadata[str(user.id)]))


            
            if i ==len(participant_list)-1:
                shares[user]=total_amount-comulative_sum
            else:

                share=(total_amount*percentage/Decimal("100")).quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP
                )
                shares[user]=share
                comulative_sum +=share

        return shares
