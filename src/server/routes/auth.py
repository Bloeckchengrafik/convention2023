import os
import subprocess

import yubico
from fastapi import APIRouter

auth_router = APIRouter()

# There should be a file "admin_serial.txt" in the root directory of the project. If there is not, we will
# create one and ask the user to enter the serial number of the YubiKey they want to use as the admin key.
admin = ""
if not os.path.exists("admin_serial.txt"):
    with open("admin_serial.txt", "w") as f:
        admin = input("Enter the serial number of the YubiKey you want to use as the admin key: ")
        f.write(admin)

# If the file exists, we will read the serial number from it.
else:
    with open("admin_serial.txt", "r") as f:
        admin = f.read()


@auth_router.get("/is_authenticated")
def is_authenticated():
    """
    Checks if the user is authenticated.
    """
    try:
        yubikey = yubico.find_yubikey(debug=False)
        if str(yubikey.serial()) == admin:
            out = subprocess.check_output(["gpg", "--card-status"])
            name = "Unknown"
            for line in out.splitlines():
                if "Name " in str(line):
                    # go to that line and get the name
                    name = str(line).split(":")[1].split("\\n")[0].removesuffix("'")
                    break

            return {"ok": True, "error": f"Welcome back, {name}!"}
        else:
            return {"ok": False, "error": "Invalid Key SID"}
    except yubico.yubico_exception.YubicoError:
        return {"ok": False, "error": "Authentication failed."}
