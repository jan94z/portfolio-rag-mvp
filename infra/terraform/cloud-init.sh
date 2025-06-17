#!/bin/bash
set -e

# Install Docker
apt-get update
apt-get install -y docker.io docker-compose

# Install Nginx and Certbot
apt-get install -y nginx certbot python3-certbot-nginx

# Enable and start services
systemctl enable --now docker
systemctl enable --now nginx

# Place your nginx config (e.g., from S3 or hardcoded here)
cat > /etc/nginx/sites-available/hire-jan.de <<'EOF'
# Redirect all HTTP to HTTPS
server {
    listen 80;
    server_name hire-jan.de www.hire-jan.de;
    return 301 https://$host$request_uri;
}

# HTTPS server block
server {
    listen 443 ssl http2;
    server_name hire-jan.de www.hire-jan.de;

    ssl_certificate /etc/letsencrypt/live/hire-jan.de/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/hire-jan.de/privkey.pem;

    # Strong SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Increase client_max_body_size if you upload large files
    client_max_body_size 100M;

    # Proxy all requests to Streamlit
    location / {
        proxy_pass http://localhost:8501;

        # Websocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Proper headers for Streamlit
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Remove Accept-Encoding to avoid double compression issues
        proxy_set_header Accept-Encoding "";
    }

    # Optional: Serve Let's Encrypt challenge for renewals
    location /.well-known/acme-challenge/ {
        root /var/www/html;
        try_files $uri =404;
    }
}
EOF

ln -sf /etc/nginx/sites-available/hire-jan.de /etc/nginx/sites-enabled/hire-jan.de
nginx -t && systemctl reload nginx

# (Optionally) Get certs (only if DNS is ready)
certbot --nginx -d hire-jan.de -d www.hire-jan.de --non-interactive --agree-tos -m your@email.com

