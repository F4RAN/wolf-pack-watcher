# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Installing Python 3..."
    sudo apt update
    sudo apt install -y python3
fi
if ! command -v pip3 &> /dev/null; then
    echo "Pip 3 is not installed. Installing Python 3..."
    sudo apt update
    sudo apt install -y python3-pip
fi
# Check if npm is installed
if command -v node &> /dev/null || ! command -v npm &> /dev/null; then
    echo "npm is not installed. Installing npm..."
    # Install node and npm
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - &&\
    sudo apt install -y nodejs
fi

# Check if PM2 is installed
if ! command -v pm2 &> /dev/null; then
    echo "PM2 is not installed. Installing PM2..."
    sudo npm install -g pm2
fi

if ! command -v unzip &> /dev/null; then
    echo "Unzip is not installed. Installing PM2..."
    sudo apt install unzip
fi

# Check if the project folder exists and remove it if it does
if [ -d "wolf-pack-watcher-main" ]; then
    echo "Previous project folder exists. Removing..."
    rm -rf wolf-pack-watcher-main
fi

# Download WOLF_PACK_WATCHER repo
echo "Downloading the file..."
wget -qO wolf-pack-watcher.zip https://github.com/F4RAN/wolf-pack-watcher/archive/refs/heads/main.zip

# Unzip the file
echo "Unzipping the file..."
unzip -q wolf-pack-watcher.zip

# Cleanup - remove the zip file
rm wolf-pack-watcher.zip

# Change to the project directory
echo "Changing to project directory..."
# shellcheck disable=SC2164
cd wolf-pack-watcher-main

# install project dependencies and complete setup
pip3 install -r requirements.txt
python3 setup_channel.py
python3 setup_telegram.py
# Run app.py with PM2
echo "Running app.py with PM2..."
pm2 start app.py --interpreter python3 --name wolf-pack-watcher
echo "Installation completed successfully! You can access Wolf Pack Watcher. \n By F4RAN: https://github.com/F4RAN/wolf-pack-watcher"


