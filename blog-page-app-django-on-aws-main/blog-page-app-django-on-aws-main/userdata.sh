#!/bin/bash
# userdata.sh - sanitized
# - update packages
yum update -y

# install python and other deps
yum install -y python3 git

# clone your app (example)
cd /home/ec2-user
git clone https://github.com/yourusername/your-repo.git app
cd app

# create venv and install requirements
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# ensure environment variables are set via systemd service or /etc/profile.d/myenv.sh
cat <<'EOF' > /etc/profile.d/app_env.sh
export DJANGO_SECRET_KEY='REPLACE_LOCALLY'
export DEBUG='False'
export DB_HOST='your-rds-host'
export DB_USER='your-db-user'
# DO NOT put DB_PASSWORD here; use Secrets Manager or Parameter Store.
EOF

# start your app (example using gunicorn and systemd — implement properly)
# systemctl enable --now myapp.service

# End of userdata
