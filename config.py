class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'system'  # Make sure this matches your MySQL password
    MYSQL_DB = 'ecommerce'
    SECRET_KEY = 'string12345'
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True
    
    # Cookie configuration
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = 'Lax'
