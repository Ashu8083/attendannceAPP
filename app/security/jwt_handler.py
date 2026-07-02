## responsibility of JWT handler
# * create JWT
# * decode JWT
# * verify expiration
# * verify signature



def create_access_token (): # life spam will 5 min (for revoke , revoke the user directly )
    return
def create_refresh_token(token): # life spam will 1 week generate new token on the use of the access token
    return
def decode_token(user):
    return
def verify_refresh_token (token):  # store in the db as token or in the device table
    return
def verify_access_token(user): # depends on the expiration and user details for validate
    return








