# social-ai-portrait

### Deploy order:

1. Create `.env` file based on `.env.example`
2. `mkdir keys`
3. Create RSA private and public keys and put them to `./keys`
   1. `openssl genrsa -traditional -out ./keys/private_key.pem 2048`
   2. `openssl rsa -in ./keys/private_key.pem -RSAPublicKey_out -out ./keys/public_key.pem`
4. Start website (nginx) on port 80 (HTTP)
   1. In `./nginx/nginx.conf` change last line from `include conf.d/prod.conf;` to `include conf.d/test.conf;` 
   2. `sudo docker compose up --build`
5. Retrieve SSL certificates from let's encrypt using certbot
   1. `sudo docker compose -f docker-compose-certbot.yml run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d socialaiprofile.top`
6. Change nginx config to use configuration for port 443 (HTTPS)
   1. In `./nginx/nginx.conf` change last line from `include conf.d/test.conf;` to `include conf.d/prod.conf;` 
   2. Restart nginx or docker container with nginx `docker restart nginx`
   3. Check website opens using HTTPS and HTTP redirects to HTTPS
7. Renew SSL certificate 
`sudo docker compose -f docker-compose-certbot.yml run --rm certbot --force-renew`