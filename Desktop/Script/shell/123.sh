#!/bin/sh

python setup.py py2app

scp -r /Users/saseny/dist/MyApp.app bundle@172.22.145.157:/Users/bundle/Desktop/

rm -rf /Users/saseny/build
rm -rf /Users/saseny/dist