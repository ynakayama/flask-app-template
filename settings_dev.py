class Settings(object):

    app_name = "Flask アプリケーション"
    sid = '9999'
    root = ''
    envrionment = 'development'
    japanese_calendar = '0'
    session_timeout = 1800

    connection_config = {
        'host' :     '127.0.0.1',
        'port' :     '5432',
        'database' : 's9999',
        'user' :     's9999',
        'password' : 's9999'
    }

    available_screens = [
        'dashboard'
    ]
