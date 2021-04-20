#!/usr/bin/env bash

# cert : /etc/letsencrypt/live/stg.skyneto.com/fullchain.pem
# key: /etc/letsencrypt/live/stg.skyneto.com/privkey.pem

# Step 1 — Installing Certbot
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install python-certbot-nginx

# Step 2 — Setting up Nginx
sudo nano /etc/nginx/sites-available/default
# change to server_name: example.com www.example.com

# verify the syntax of your configuration edits
sudo nginx -t

sudo systemctl reload nginx

# Step 3 — Obtaining an SSL Certificate
sudo certbot --nginx -d example.com -d www.example.com


# Step 4 - Restart
sudo systemctl restart nginx