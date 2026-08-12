import bittensor as bt
from bittensor.balance import Balance


class Proxy:
    def __init__(self, network: str):
        """
        Initialize the RonProxy object.
        
        Args:
            proxy_wallet: Proxy wallet address
            network: Network name
            delegator: Delegator address
        """
        self.network = network
        self.subtensor = bt.Subtensor(network)

    def add_stake(
        self, 
        proxy_wallet: bt.Wallet,
        delegator: str,
        netuid: int, 
        hotkey: str, 
        amount: Balance, 
        tolerance: float = 0.005,
    ) -> tuple[bool, str]:
        """
        Add stake to a subnet.
        
        Args:
            proxy_wallet: Proxy wallet
            netuid: Network/subnet ID
            hotkey: Hotkey address
            amount: Amount to stake
            tolerance: Tolerance for stake amount
        """
        free_balance = self.subtensor.balances.get(delegator)
        print(f"free_balance: {free_balance}")

        info = self.subtensor.runtime(
            bt.runtime_api.SubnetInfoRuntimeApi.get_dynamic_info, [netuid]
        )
        if not info:
            return False, f"Subnet with netuid {netuid} does not exist"

        # Pass the unlocked coldkey Keypair (a Signer), not the Wallet.
        # execute() wraps a Wallet in a fresh WalletSigner each call and would
        # re-prompt for the password even after unlock_coldkey().
        signer = proxy_wallet.coldkey
        try:
            result = self.subtensor.execute(
                bt.AddStake(
                    hotkey_ss58=hotkey,
                    netuid=netuid,
                    amount_tao=amount.tao,
                    slippage_protection=True,
                    rate_tolerance=tolerance,
                ),
                signer,
                proxy_for=delegator,
                proxy_type="Staking",
                wait_for_inclusion=True,
                wait_for_finalization=False,
            )
            error_message = result.message
        except Exception as e:
            error_message = str(e)
            result = None

        new_free_balance = self.subtensor.balances.get(delegator)
        if new_free_balance.rao < free_balance.rao:
            return True, "Stake added successfully"
        if result is not None and result.success:
            return True, "Stake added successfully"
        return False, f"Error: {error_message}"


    def remove_stake(
        self, 
        proxy_wallet: bt.Wallet,
        delegator: str,
        netuid: int,
        hotkey: str,
        amount: Balance,
        tolerance: float = 0.005,
    ) -> tuple[bool, str]:
        """
        Remove stake from a subnet.
        
        Args:
            proxy_wallet: Proxy wallet
            netuid: Network/subnet ID
            hotkey: Hotkey address
            amount: Amount to unstake (if not using --all)
            all: Whether to unstake all available balance
        """
        info = self.subtensor.runtime(
            bt.runtime_api.SubnetInfoRuntimeApi.get_dynamic_info, [netuid]
        )
        if not info:
            return False, f"Subnet with netuid {netuid} does not exist"

        # amount is subnet alpha (or TAO on netuid 0); leave 1 rao dust like before
        amount_alpha = max(amount.rao - 1, 0) / 1e9
        print(f"amount: {amount.rao}")

        free_balance = self.subtensor.balances.get(delegator)

        # Pass unlocked coldkey Keypair so execute does not re-prompt.
        signer = proxy_wallet.coldkey
        try:
            result = self.subtensor.execute(
                bt.RemoveStake(
                    hotkey_ss58=hotkey,
                    netuid=netuid,
                    amount_alpha=amount_alpha,
                    slippage_protection=True,
                    rate_tolerance=tolerance,
                ),
                signer,
                proxy_for=delegator,
                proxy_type="Staking",
                wait_for_inclusion=True,
                wait_for_finalization=False,
            )
            error_message = result.message
        except Exception as e:
            error_message = str(e)
            result = None

        new_free_balance = self.subtensor.balances.get(delegator)
        if new_free_balance.rao > free_balance.rao:
            return True, "Stake removed successfully"
        if result is not None and result.success:
            return True, "Stake removed successfully"
        return False, f"Error: {error_message}"


if __name__ == "__main__":
    proxy_wallet = bt.Wallet(name="black")
    delegator = "5F5WLLEzDBXQDdTzDYgbQ3d3JKbM15HhPdFuLMmuzcUW5xG2"
    amount = input("Enter amount to stake: ")
    netuid = input("Enter netuid: ")
    proxy_wallet.unlock_coldkey()
    proxy = Proxy("finney")
    is_success, error_message = proxy.add_stake(
        proxy_wallet,
        delegator,
        int(netuid),
        "5F5WLLEzDBXQDdTzDYgbQ3d3JKbM15HhPdFuLMmuzcUW5xG2",
        Balance.from_tao(int(amount)),
    )
    print(is_success, error_message)
