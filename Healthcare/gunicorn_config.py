# gunicorn_config.py

bind = "0.0.0.0:8000"

# workers = 4  # Adjust based on your server's resources
# worker_connections = 1000
# threads = 4

# SSL non funziona. Too bad!
#
#certfile = "/etc/letsencrypt/live/healthcareapp.xyz/fullchain.pem"
#keyfile = "/etc/letsencrypt/live/healthcareapp.xyz/privkey.pem"
cert_reqs = 1;