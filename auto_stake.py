import sys
import os
import time

# Add the parent directory to the Python search path (sys.path)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    
import bittensor as bt
from typing import List

from app.constants import tao5_HOTKEY
from app.core.config import settings
from app.services.proxy import Proxy
from utils.logger import logger


WALLET_NAMES: List[str] = ["spa"]
DELEGATORS: List[str] = ["5G2Qr3K4Nxyrmo6FaDc9go6g4UC2RR4ghcXsKypdy4JT1rLe"]

if __name__ == '__main__':
    netuid = int(input("Enter the netuid: "))
    lower_threshold = float(input("Enter the lower threshold: "))
    wallet_name = input("Enter the wallet name(default is spa): ") or WALLET_NAMES[0]
    delegator = DELEGATORS[WALLET_NAMES.index(wallet_name)]
    dest_hotkey = input("Enter the dest hotkey (default is tao5): ") or tao5_HOTKEY
    amount_to_stake = float(input("Enter the amount_to_stake(default is 1): ") or 1)
    tolerance = float(input("Enter the tolerance(default is 0.01): ") or 0.01)

    proxy = Proxy(network=settings.NETWORK)
    proxy.init_runtime()
    subtensor = bt.Subtensor(network=settings.NETWORK)
    wallet = bt.Wallet(name=wallet_name)
    wallet.unlock_coldkey()

    amount_balance = subtensor.get_stake(
        coldkey_ss58=delegator,
        hotkey_ss58=dest_hotkey,
        netuid=netuid
    )

    print("Press Ctrl+C to stop the script")
    print(f"Wallet: {wallet_name}, Delegator: {delegator}, Dest Hotkey: {dest_hotkey}, Amount: {amount_balance.tao}, Tolerance: {tolerance}")

    time.sleep(10)
    while True:
        try:
            subnet = subtensor.subnet(netuid=netuid)
            if subnet is None:
                logger.error(f"Subnet is None for netuid: {netuid}")
                continue

            amount_balance = subtensor.get_stake(
                coldkey_ss58=delegator,
                hotkey_ss58=dest_hotkey,
                netuid=netuid
            )
            # print(amount_balance)

            # if amount_balance.tao > 1:
            #     logger.info(f"Amount balance is more than 1 TAO for netuid: {netuid}. Skipping...")
            #     continue
            
            alpha_price = subnet.alpha_to_tao(1)
            logger.info(f"Current alpha token price: {alpha_price} TAO")
            
            if lower_threshold != -1 and alpha_price > bt.Balance.from_tao(lower_threshold):
                logger.info(f"Current price {alpha_price} TAO is above lower_threshold {lower_threshold} TAO. Skipping...")
                continue
            print("\n----------------------------------------------------------------------------------------------------------------------------------------")
            success, msg = proxy.add_stake(
                proxy_wallet=wallet,
                delegator=delegator,
                netuid=netuid,
                hotkey=dest_hotkey,
                amount=bt.Balance(amount_to_stake),
                tolerance=tolerance,
            )
            print("----------------------------------------------------------------------------------------------------------------------------------------\n")

            if success:
                break
            else:
                print("====================================================================Failed=============================================")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
