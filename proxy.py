#!/usr/bin/env python3
"""
Proxy script for blockchain staking operations.
"""

import argparse
import sys
from modules import RonProxy
from bittensor.utils.balance import Balance


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Proxy script for blockchain staking operations",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add stake command
    add_parser = subparsers.add_parser('addstake', help='Add stake to a subnet')
    add_parser.add_argument('--netuid', type=int, required=True, help='Network/subnet ID')
    add_parser.add_argument('--hotkey', type=str, required=True, help='Hotkey address')
    add_parser.add_argument('--amount', type=float, help='Amount to stake')
    add_parser.add_argument('--tolerance', type=float, default=0.05, help='Tolerance for stake')
    add_parser.add_argument('--name', type=str, default=".env", help='Specify the environment')
    
    # Remove stake command
    remove_parser = subparsers.add_parser('removestake', help='Remove stake from a subnet')
    remove_parser.add_argument('--netuid', type=int, required=True, help='Network/subnet ID')
    remove_parser.add_argument('--hotkey', type=str, required=True, help='Hotkey address')
    remove_parser.add_argument('--amount', type=float, default=0, help='Amount to unstake')
    remove_parser.add_argument('--all', action='store_true', help='Remove all staked balance')
    remove_parser.add_argument('--tolerance', type=float, default=0.05, help='Tolerance for stake')
    remove_parser.add_argument('--name', type=str, default=".env", help='Specify the environment')
    
    # Swap stake command
    swap_parser = subparsers.add_parser('swapstake', help='Swap stake between subnets')
    swap_parser.add_argument('--hotkey', type=str, required=True, help='Hotkey address')
    swap_parser.add_argument('--origin-netuid', type=int, required=True, help='Source subnet ID')
    swap_parser.add_argument('--dest-netuid', type=int, required=True, help='Destination subnet ID')
    swap_parser.add_argument('--amount', type=float, default=0, help='Amount to swap')
    swap_parser.add_argument('--all', action='store_true', help='Swap all available balance')
    swap_parser.add_argument('--name', type=str, default=".env", help='Specify the environment')
    
    # Move stake command
    move_parser = subparsers.add_parser('movestake', help='Move stake between subnets')
    move_parser.add_argument('--origin-hotkey', type=str, required=True, help='Hotkey address')
    move_parser.add_argument('--destination-hotkey', type=str, required=True, help='Source subnet ID')
    move_parser.add_argument('--origin-netuid', type=int, required=True, help='Destination subnet ID')
    move_parser.add_argument('--destination-netuid', type=int, default=0, help='Amount to swap')
    move_parser.add_argument('--amount', type=float, default=0, help='Amount to swap')
    move_parser.add_argument('--all', action='store_true', help='Swap all available balance')
    move_parser.add_argument('--name', type=str, default=".env", help='Specify the environment')

    register_parser = subparsers.add_parser('register', help='Swap stake between subnets')
    register_parser.add_argument('--hotkey', type=str, required=True, help='Hotkey address')
    register_parser.add_argument('--netuid', type=int, required=True, help='Source subnet ID')
    register_parser.add_argument('--name', type=str, default=".env", help='Specify the environment')
    
    return parser


def validate_args(args: argparse.Namespace) -> bool:
    """Validate argument combinations."""
    if args.command == 'addstake':
        if not args.amount:
            print("Error: Must specify --amount")
            return False
    
    elif args.command in ['removestake', 'swapstake', 'movestake']:    
        if not args.amount and not args.all:
            print("Error: Must specify either --amount or --all")
            return False
        if args.amount and args.all:
            print("Error: Cannot specify both --amount and --all")
            return False
    
    return True


def main():
    """Main entry point."""
    # Import environment variables
    from dotenv import load_dotenv
    import os
    # load_dotenv()
    
    # network = os.getenv('NETWORK')
    # delegator = os.getenv('DELEGATOR')
    # proxy_wallet = os.getenv('PROXY_WALLET')
    
    # # Validate environment variables
    # if not network or not delegator or not proxy_wallet:
    #     print("Error: Missing environment variables")
    #     sys.exit(1)

    # Create parser
    parser = create_parser()
    
    # Parse arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    if args.name == ".env":
        env_file = f".env"
    elif args.name == "jeet":
        env_file = f".env.tobi.jeet" 
    elif args.name == "longterm":
        env_file = f".env.tobi.longterm" 
    elif args.name == "whale":
        env_file = f".env.tobi.whale" 
    elif args.name == "beta":
        env_file = f".env.tobi.beta"
    elif args.name == "alpha":
        env_file = f".env.tobi.alpha"
    elif args.name == "atel":
        env_file = f".env.jjpes.atel" 
    elif args.name == "jjcom":
        env_file = f".env.jjpes.jjcom" 
    elif args.name == "midas":
        env_file = f".env.thunder.midas" 
    elif args.name == "lazy":
        env_file = f".env.thunder.lazyterry" 
    elif args.name == "const":
        env_file = f".env.druid.const" 
    elif args.name == "taomind":
        env_file = f".env.druid.taomind" 
    elif args.name == "terry":
        env_file = f".env.druid.terry" 
    elif args.name == "gang":
        env_file = f".env.sky.gang" 
    elif args.name == "izo":
        env_file = f".env.sky.izo" 
    elif args.name == "sky":
        env_file = f".env.sky.sky"
    elif args.name == "w1":
        env_file = f".env.eros.w1" 
    elif args.name == "w2":
        env_file = f".env.eros.w2" 
    elif args.name == "aeth":
        env_file = f".env.tobi.aeth"
    elif args.name == "gunner":
        env_file = f".env.tobi.gunner"

    print(f"Env file: {env_file}")

    # Load the specified .env file
    if os.path.exists(env_file):
        load_dotenv(env_file, override=True)
    else:
        raise FileNotFoundError(f"The environment file {env_file} does not exist.")
    
    network = os.getenv('NETWORK')
    delegator = os.getenv('DELEGATOR')
    proxy_wallet = os.getenv('PROXY_WALLET')

    print(f"Network: {network}")
    print(f"Delegator: {delegator}")
    print(f"Proxy wallet: {proxy_wallet}")
    if args.command == "register":
        proxy_hotkey = args.hotkey
        print(f"Hotkey: {proxy_hotkey}")
    else:
        proxy_hotkey = None

    if not network or not delegator or not proxy_wallet:
        print("Error: Missing environment variables")
        sys.exit(1)

    
    # Validate arguments
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if not validate_args(args):
        sys.exit(1)
        
    # Initialize RonProxy object
    ron_proxy = RonProxy(
        proxy_wallet=proxy_wallet,
        network=network,
        delegator=delegator,
        proxy_hotkey=proxy_hotkey
    )
    print(f"Initialized RonProxy object for {network} network")
    
    try:
        if args.command == 'addstake':
            ron_proxy.add_stake(
                netuid=args.netuid,
                hotkey=args.hotkey,
                amount=Balance.from_tao(args.amount),
                tolerance=args.tolerance,
            )
        elif args.command == 'removestake':
            ron_proxy.remove_stake(
                netuid=args.netuid,
                hotkey=args.hotkey,
                amount=Balance.from_tao(args.amount, netuid=args.netuid),
                all=args.all,
                tolerance=args.tolerance,
            )
        elif args.command == 'swapstake':
            ron_proxy.swap_stake(
                hotkey=args.hotkey,
                origin_netuid=getattr(args, 'origin_netuid'),
                dest_netuid=getattr(args, 'dest_netuid'),
                amount=Balance.from_tao(args.amount, args.origin_netuid),
                all=args.all,
            )
        elif args.command == 'movestake':
            ron_proxy.move_stake(
                origin_hotkey=args.origin_hotkey,
                destination_hotkey=args.destination_hotkey,
                origin_netuid=args.origin_netuid,
                destination_netuid=args.destination_netuid,
                amount=Balance.from_tao(args.amount, args.origin_netuid),
                all=args.all,
            )
        elif args.command == 'register':
            ron_proxy.burned_register(
                hotkey=args.hotkey,
                netuid=args.netuid,
            )
    
    except Exception as e:
        print(f"qqqqError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
