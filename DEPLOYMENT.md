# Deployment Guide

This guide covers deploying the Whistleblower Reporting System to production.

## Prerequisites

- Linux server (Ubuntu 20.04+ recommended)
- Docker and Docker Compose installed
- Domain name configured
- SSL certificate (Let's Encrypt recommended)

## Production Deployment Steps

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
```

### 2. Clone Repository

```bash
git clone https://github.com/jagomes445/whistleblower-system.git
cd whistleblower-system
```

### 3. Configure Environment

```bash
cp .env.example .env
nano .env
```

Update the following critical values:

```bash
# Django Settings
DJANGO_SECRET_KEY=<generate-strong-random-key>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database (use strong passwords)
POSTGRES_PASSWORD=<generate-strong-password>

# Email (configure SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=<your-sendgrid-api-key>
DEFAULT_FROM_EMAIL=noreply@your-domain.com

# Frontend URL
FRONTEND_URL=https://your-domain.com
CORS_ALLOWED_ORIGINS=https://your-domain.com

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 4. Generate Django Secret Key

```bash
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 5. SSL Certificate Setup (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Generate certificate
sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com
```

### 6. Update Nginx Configuration

Edit `nginx/nginx.conf` to include SSL:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    client_max_body_size 20M;
    
    # Frontend
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }
    
    # Backend API
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # Django Admin
    location /admin/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # Static files
    location /static/ {
        alias /app/staticfiles/;
    }
    
    # Media files
    location /media/ {
        alias /app/media/;
    }
}
```

### 7. Update Production Docker Compose

Edit `docker-compose.prod.yml` to mount SSL certificates:

```yaml
nginx:
  build:
    context: ./nginx
    dockerfile: Dockerfile
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - static_volume:/app/staticfiles
    - media_volume:/app/media
    - frontend_build:/usr/share/nginx/html
    - /etc/letsencrypt:/etc/letsencrypt:ro
  depends_on:
    - backend
    - frontend
  restart: always
```

### 8. Build Frontend with Production API URL

Create `frontend/.env.production`:

```bash
VITE_API_URL=https://your-domain.com/api
```

### 9. Start Production Stack

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

### 10. Initialize Database

```bash
# Run migrations
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput

# Create superuser
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

### 11. Verify Deployment

1. Visit https://your-domain.com
2. Test user registration
3. Test report submission
4. Check Django admin: https://your-domain.com/admin
5. Verify email notifications are working

## Security Checklist

- [ ] Changed Django SECRET_KEY
- [ ] Set DJANGO_DEBUG=False
- [ ] Configured strong database passwords
- [ ] Set up SSL certificates
- [ ] Configured proper ALLOWED_HOSTS
- [ ] Enabled HTTPS redirect
- [ ] Set secure cookie flags
- [ ] Configured CORS properly
- [ ] Set up email notifications
- [ ] Backed up encryption keys
- [ ] Set up database backups
- [ ] Configured firewall rules
- [ ] Set up monitoring/logging

## Backup Strategy

### Database Backup

```bash
# Create backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U whistleblower_user whistleblower_db > backup_$(date +%Y%m%d).sql

# Restore backup
docker-compose -f docker-compose.prod.yml exec -T db psql -U whistleblower_user whistleblower_db < backup_20240115.sql
```

### Automated Backups

Add to crontab:

```bash
# Daily backup at 2 AM
0 2 * * * cd /path/to/whistleblower-system && docker-compose -f docker-compose.prod.yml exec db pg_dump -U whistleblower_user whistleblower_db > backups/backup_$(date +\%Y\%m\%d).sql
```

## Monitoring

### Log Access

```bash
# View all logs
docker-compose -f docker-compose.prod.yml logs

# View backend logs
docker-compose -f docker-compose.prod.yml logs backend

# View nginx logs
docker-compose -f docker-compose.prod.yml logs nginx

# Follow logs in real-time
docker-compose -f docker-compose.prod.yml logs -f
```

### Health Checks

```bash
# Check running services
docker-compose -f docker-compose.prod.yml ps

# Check resource usage
docker stats
```

## Updating the Application

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up --build -d

# Run new migrations
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs backend

# Check configuration
docker-compose -f docker-compose.prod.yml config
```

### Database Connection Issues

```bash
# Check database is running
docker-compose -f docker-compose.prod.yml ps db

# Test database connection
docker-compose -f docker-compose.prod.yml exec backend python manage.py dbshell
```

### SSL Certificate Renewal

```bash
# Renew certificates (Let's Encrypt)
sudo certbot renew

# Reload nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

## Performance Optimization

### Database Optimization

```bash
# Run VACUUM
docker-compose -f docker-compose.prod.yml exec db psql -U whistleblower_user -d whistleblower_db -c "VACUUM ANALYZE;"
```

### Scale Workers

Update `docker-compose.prod.yml` to increase Gunicorn workers:

```yaml
backend:
  command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 8 --timeout 120
```

## Support

For deployment issues:
- Check logs first
- Review security checklist
- Consult documentation
- Open an issue on GitHub

## Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
