#!/usr/bin/env python3
"""Change the MAC address of a network interface.

Examples:
Linux:
  sudo python3 change_mac_address.py eth0 --random
  sudo python3 change_mac_address.py wlan0 --mac 02:11:22:33:44:55

Windows (PowerShell as Administrator):
  python change_mac_address.py "Wi-Fi" --random
  python change_mac_address.py "Ethernet" --mac 02:11:22:33:44:55

Safe preview mode on either OS:
  python3 change_mac_address.py eth0 --random --dry-run
"""

from __future__ import annotations

import argparse
import platform
import random
import re
import subprocess
import sys

MAC_REGEX = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")


def validate_mac(mac: str) -> str:
    if not MAC_REGEX.fullmatch(mac):
        raise argparse.ArgumentTypeError(
            "Invalid MAC format. Use XX:XX:XX:XX:XX:XX (hex bytes)."
        )
    return mac.lower()


def generate_locally_administered_mac() -> str:
    """Generate a random unicast, locally administered MAC address."""
    first_octet = random.randint(0x00, 0xFF)
    first_octet = (first_octet | 0x02) & 0xFE
    octets = [first_octet] + [random.randint(0x00, 0xFF) for _ in range(5)]
    return ":".join(f"{b:02x}" for b in octets)


def run(cmd: list[str], dry_run: bool) -> None:
    if dry_run:
        print("[DRY-RUN]", " ".join(cmd))
        return
    subprocess.run(cmd, check=True)


def change_mac_linux(interface: str, new_mac: str, dry_run: bool) -> None:
    run(["ip", "link", "set", "dev", interface, "down"], dry_run)
    run(["ip", "link", "set", "dev", interface, "address", new_mac], dry_run)
    run(["ip", "link", "set", "dev", interface, "up"], dry_run)


def change_mac_windows(interface: str, new_mac: str, dry_run: bool) -> None:
    # Set-NetAdapter advanced property expects no separators.
    mac_no_colons = new_mac.replace(":", "")
    ps_cmd = (
        "Set-NetAdapterAdvancedProperty "
        f"-Name '{interface}' "
        "-RegistryKeyword 'NetworkAddress' "
        f"-RegistryValue '{mac_no_colons}'"
    )
    run(["powershell", "-NoProfile", "-Command", ps_cmd], dry_run)

    # Bounce interface to apply the new MAC immediately.
    restart_cmd = f"Restart-NetAdapter -Name '{interface}' -Confirm:$false"
    run(["powershell", "-NoProfile", "-Command", restart_cmd], dry_run)


def change_mac(interface: str, new_mac: str, dry_run: bool) -> None:
    system = platform.system().lower()
    if system == "linux":
        change_mac_linux(interface, new_mac, dry_run)
        return
    if system == "windows":
        change_mac_windows(interface, new_mac, dry_run)
        return
    raise OSError(f"Unsupported OS: {platform.system()}. Supported: Linux, Windows.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Change a network interface MAC address")
    parser.add_argument(
        "interface",
        help="Linux interface (e.g. eth0, wlan0) or Windows adapter name (e.g. Ethernet)",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--mac", type=validate_mac, help="Set a specific MAC address")
    group.add_argument("--random", action="store_true", help="Generate and set a random MAC")

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without making changes",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target_mac = args.mac if args.mac else generate_locally_administered_mac()

    try:
        change_mac(args.interface, target_mac, args.dry_run)
    except FileNotFoundError:
        print(
            "Error: required command not found ('ip' on Linux or PowerShell on Windows).",
            file=sys.stderr,
        )
        return 1
    except OSError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as exc:
        print(f"Failed to change MAC address: {exc}", file=sys.stderr)
        print("Tip: run with administrator/root privileges.", file=sys.stderr)
        return 1

    print(f"MAC address for {args.interface} set to {target_mac}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
