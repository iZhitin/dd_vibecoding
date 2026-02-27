#!/bin/bash

# Check for docker compose (v2)
if ! docker compose version > /dev/null 2>&1; then
  echo 'Error: docker compose (v2) is not installed.' >&2
  exit 1
fi

domains=(ddictionary.org)
rsa_key_size=4096
data_path="./data/certbot"
email="admin@ddictionary.org" 
staging=0 

if [ ! -e "$data_path/conf/options-ssl-nginx.conf" ] || [ ! -e "$data_path/conf/ssl-dhparams.pem" ]; then
  echo "### Downloading recommended TLS parameters ..."
  mkdir -p "$data_path/conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "$data_path/conf/options-ssl-nginx.conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "$data_path/conf/ssl-dhparams.pem"
  echo
fi

echo "### Starting nginx with HTTP-only config ..."
cp nginx/nginx.conf.init nginx/nginx.conf
docker compose up --force-recreate -d nginx
echo

echo "### Requesting Let's Encrypt certificate for $domains ..."
domain_args=""
for domain in "${domains[@]}"; do
  domain_args="$domain_args -d $domain"
done

case "$email" in
  "") email_arg="--register-unsafely-without-email" ;;
  *) email_arg="-m $email" ;;
esac

if [ $staging != "0" ]; then staging_arg="--staging"; fi

docker compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    $staging_arg \
    $email_arg \
    $domain_args \
    --rsa-key-size $rsa_key_size \
    --agree-tos \
    --force-renewal" certbot
echo

echo "### Switching to HTTPS config ..."
cp nginx/nginx.conf.prod nginx/nginx.conf

echo "### Reloading nginx ..."
docker compose exec nginx nginx -s reload
