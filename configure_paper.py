"""Configure Alpaca paper credentials locally without displaying their values."""
from getpass import getpass
from pathlib import Path
import os


def main():
    from dotenv import set_key
    path = Path(__file__).resolve().parent / ".env"
    print("Use the Key ID and Secret Key from your Alpaca PAPER account.")
    print("Values are hidden as you type. They remain on this computer.")
    key = getpass("Paper Key ID: ").strip()
    secret = getpass("Paper Secret Key: ").strip()
    if not key or not secret:
        raise SystemExit("Both credentials are required; nothing was changed.")
    if not path.exists():
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(fd)
    os.chmod(path, 0o600)
    set_key(str(path), "ALPACA_API_KEY", key)
    set_key(str(path), "ALPACA_API_SECRET", secret)
    print("Paper credentials saved. Run the connection check before trading.")


if __name__ == "__main__":
    main()
