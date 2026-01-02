import base64
import requests
import os
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

# Load secrets from Streamlit
import streamlit as st

NEYNAR_API_KEY = st.secrets["NEYNAR_API_KEY"]
APP_FID = st.secrets["APP_FID"]
APP_ECDSA_PRIVATE_KEY = st.secrets["APP_ECDSA_PRIVATE_KEY"]


def generate_signer_keypair():
    """Generate a new Ed25519 signer keypair."""
    private_key = Ed25519PrivateKey.generate()
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    return {
        "private_key": base64.b64encode(private_bytes).decode(),
        "public_key": base64.b64encode(public_key).decode()
    }


def request_signer_approval(public_key_b64):
    """Request signer approval via Neynar."""
    url = "https://api.neynar.com/v2/farcaster/signer"
    headers = {
        "Content-Type": "application/json",
        "api_key": NEYNAR_API_KEY
    }
    payload = {
        "app_fid": int(APP_FID),
        "signer_public_key": public_key_b64,
        "app_signature": sign_public_key(public_key_b64)
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


def publish_cast(signer_uuid, text, parent_url=None):
    """Publish a cast using Neynar."""
    url = "https://api.neynar.com/v2/farcaster/cast"
    headers = {
        "Content-Type": "application/json",
        "api_key": NEYNAR_API_KEY
    }
    payload = {
        "signer_uuid": signer_uuid,
        "text": text
    }
    if parent_url:
        payload["parent_url"] = parent_url
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


def sign_public_key(public_key_b64):
    """Sign the public key using the app's ECDSA private key."""
    from eth_account import Account
    from eth_account.messages import encode_defunct

    acct = Account.from_key(APP_ECDSA_PRIVATE_KEY)
    message = encode_defunct(text=public_key_b64)
    signed = Account.sign_message(message, private_key=APP_ECDSA_PRIVATE_KEY)
    return signed.signature.hex()
