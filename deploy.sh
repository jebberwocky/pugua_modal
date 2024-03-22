 #!/bin/bash
# Setup
APP_NAME="ZhouyiHexagram"
TOKEN="kG2tVqtK4LNU37dW3qqKXF9sU9guVURz"
# Helper functions
info() {
  echo -e "\033[1;34m$@\033[0m"
}

error() {
  echo -e "\033[1;31m$@\033[0m" >&2
}
 
 
 modal deploy bot.py
 curl -X POST https://api.poe.com/bot/fetch_settings/${APP_NAME}/${TOKEN}