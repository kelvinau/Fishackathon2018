import os

if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    # GAE
    pass
else:
    # LOCAL
    pass
