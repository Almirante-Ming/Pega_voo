import pyotp
import os

secret = str(os.getenv('SECRET_KEY'))
totp = pyotp.TOTP(secret)
kcode = totp.now()
