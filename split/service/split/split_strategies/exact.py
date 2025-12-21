from decimal import Decimal,ROUND_HALF_UP

from .base import SplitStrategy

class ExactSplitStrategy(SplitStrategy):
    

    def split(self, total_amount, participants, metadata=None):
 
        if not metadata:
            raise ValueError("Exact amounts are required in metadata.")

        shares = {}
        provided_total = Decimal("0.00")

        for user in participants:
            # Convert user.id to string to match the JSON key from the frontend
            user_id_str = str(user.id) 
            
            if user_id_str not in metadata:
                raise ValueError(f"Missing amount for user {user.username}")
            
            # Get the exact amount from metadata using the string key
            user_amount = Decimal(str(metadata[user_id_str]))
            shares[user] = user_amount
            provided_total += user_amount

        # Validation: The sum of provided amounts must match the total
        if provided_total != total_amount:
            raise ValueError(
                f"Sum of amounts ({provided_total}) does not match total ({total_amount})"
            )

        return shares