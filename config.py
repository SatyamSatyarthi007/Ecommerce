class Config:
    # Replace with your Railway MySQL credentials
    MYSQL_HOST = 'your-railway-host'
    MYSQL_USER = 'your-railway-username'
    MYSQL_PASSWORD = 'your-railway-password'
    MYSQL_DB = 'your-railway-database'
    
    # Flask configuration
    SECRET_KEY = 'your-secret-key'  # Change this to a secure secret key
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes
    
    # Cookie configuration
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = 'Lax'
