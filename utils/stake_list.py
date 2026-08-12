import bittensor as bt

from rich.console import Console
from rich.table import Table
from io import StringIO


def get_amount(tao_in, alpha_in, alpha_unstake_amount):
    p = tao_in * alpha_in
    alpha_in_after = alpha_in + alpha_unstake_amount
    tao_in_after = p / alpha_in_after
    return tao_in - tao_in_after


def get_stake_list(subtensor, wallet_ss58):
    stake_infos = subtensor.staking.positions(wallet_ss58)
    dynamic_infos = (
        subtensor.runtime(bt.runtime_api.SubnetInfoRuntimeApi.get_all_dynamic_info, [])
        or []
    )
    subnet_by_netuid = {}
    for info in dynamic_infos:
        if not info:
            continue
        netuid = int(info["netuid"])
        subnet_name = info.get("subnet_name") or ""
        if isinstance(subnet_name, (bytes, bytearray, list)):
            subnet_name = bytes(subnet_name).decode(errors="replace")
        token_symbol = info.get("token_symbol") or ""
        if isinstance(token_symbol, (bytes, bytearray, list)):
            token_symbol = bytes(token_symbol).decode(errors="replace")
        tao_in = int(info["tao_in"]) / 1e9
        alpha_in = int(info["alpha_in"]) / 1e9
        price = (tao_in / alpha_in) if alpha_in else 0.0
        subnet_by_netuid[netuid] = {
            "subnet_name": subnet_name,
            "tao_in": tao_in,
            "alpha_in": alpha_in,
            "price": price,
            "symbol": token_symbol,
        }

    # Create a Rich Table to display the stake_infos in a readable format

    table = Table(title="Stake Infos", show_lines=True)
    table.add_column("NetUID", justify="right", no_wrap=True)
    table.add_column("Subnet Name")
    table.add_column("Value")
    table.add_column("Stake", justify="right")
    table.add_column("Price")
    table.add_column("Hotkey SS58")

    # stake_infos is a list of StakePosition objects
    total_value = 0
    for info in stake_infos:
        subnet_info = subnet_by_netuid.get(info.netuid)
        if subnet_info is None:
            continue
        stake_amount = info.stake.amount
        value = get_amount(subnet_info["tao_in"], subnet_info["alpha_in"], stake_amount)
        table.add_row(
            str(info.netuid),
            subnet_info["subnet_name"],
            f"{value:.2f}",
            f"{stake_amount:.2f}",
            f"{subnet_info['price']:.4f}",
            info.hotkey,
        )
        total_value += value



    balance = subtensor.balances.get(wallet_ss58)
    
    console = Console(file=StringIO(), force_terminal=False)
    console.print(table)
    console.print("\n")
    console.print(
        f"Wallet:\n"
        f"  Coldkey SS58: {wallet_ss58}\n"
        f"  Free Balance: {balance}\n"
        f"  Total TAO Value (TAO): {total_value}"
    )

    table_str = console.file.getvalue()
    return table_str
    

if __name__ == "__main__":
    subtensor = bt.Subtensor("finney")
    wallet_ss58 = "5G2Qr3K4Nxyrmo6FaDc9go6g4UC2RR4ghcXsKypdy4JT1rLe"
    stake_list = get_stake_list(subtensor, wallet_ss58)    
    print(stake_list)
