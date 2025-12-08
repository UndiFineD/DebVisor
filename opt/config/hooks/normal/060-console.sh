#!/bin/sh
set -e

echo "Configuring console..."

# Enable kmscon to replace standard getty
if [ -x /usr/bin/kmscon ]; then
    echo "Enabling kmscon service..."
    systemctl enable kmscon
    
    # Mask getty on tty1 to prevent conflict/flickering
    systemctl mask getty@tty1
fi
