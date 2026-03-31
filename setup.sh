#!/bin/bash
# Autoriser ImageMagick à lire/écrire pour les sous-titres
sudo sed -i 's/policy domain="path" rights="none" pattern="@\*"/policy domain="path" rights="read|write" pattern="@\*"/g' /etc/ImageMagick-6/policy.xml