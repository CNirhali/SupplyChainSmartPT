import streamlit as st
import streamlit_authenticator as stauth

# Demo user config (replace with secure storage in production)
users = [
    {'name': 'Warehouse User', 'username': 'warehouse', 'password': 'warehouse123', 'role': 'warehouse'},
    {'name': 'Procurement User', 'username': 'procurement', 'password': 'procure123', 'role': 'procurement'},
    {'name': 'Admin User', 'username': 'admin', 'password': 'admin123', 'role': 'admin'},
]

usernames = [u['username'] for u in users]
names = [u['name'] for u in users]
passwords = [u['password'] for u in users]
roles = {u['username']: u['role'] for u in users}

def authenticate():
    """
    Authenticate user using Streamlit Authenticator. Returns (authenticator, authenticated, username, role)
    """
    authenticator = stauth.Authenticate(
        names,
        usernames,
        passwords,
        'supply_chain_auth_cookie',
        'supply_chain_auth_key',
        cookie_expiry_days=1
    )
    name, authentication_status, username = authenticator.login('Login', 'sidebar')
    role = roles.get(username) if username else None
    return authenticator, authentication_status, username, role 