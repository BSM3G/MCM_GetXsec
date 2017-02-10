#!/bin/bash

echo "Checking dependencies for python"
pip list 2>/dev/null | grep selenium &>/dev/null
if [ $? -ne 0 ]
then
    echo "Installing selenium"
    pip install selenium
fi
pip list 2>/dev/null | grep pyvirtualdisplay &>/dev/null
if [ $? -ne 0 ]
then
    echo "Installing pyvirtualdisplay"
    pip install pyvirtualdisplay
fi

if [ ! -d "./firefox" ]
then
    echo "Getting correct firefox"
    wget https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-central/firefox-54.0a1.en-US.linux-x86_64.tar.bz2
    echo "Extracting the files"
    tar -xjf firefox-54.0a1.en-US.linux-x86_64.tar.bz2
    rm firefox-54.0a1.en-US.linux-x86_64.tar.bz2

fi

firefox_bin=$PWD/firefox/firefox-bin
sed -i "s|FIREFOX_AREA|$firefox_bin|g" get_xsec.py 

if [ ! -f geckodriver ]
then
    wget https://github.com/mozilla/geckodriver/releases/download/v0.14.0/geckodriver-v0.14.0-linux64.tar.gz
    tar -xvf geckodriver-v0.14.0-linux64.tar.gz
    rm geckodriver-v0.14.0-linux64.tar.gz
fi

gecko=$(pwd -P)
sed -i "s|GECKO_PATH|$gecko|g" get_xsec.py


sleep 5s

ls /usr/bin/ | grep "xvfb" &>/dev/null
if [ $? -ne 0 ]
then
    echo "To run this without visuals, you need to install xvfb"
    echo "If you have root privileges, you will be asked to put in your password to install this"
    echo "If you do not have root privileges, exit the program here"
    echo
    echo "Please choose a number with your choice"
    select choice in "Exit" "Install"
    do
        if [ -z $choice ]
        then
            echo "Make a valid choice"
        else
            if [ $choice == "Exit" ]
            then
                echo "Exiting"
                exit 0
            elif [ $choice == "Install" ]
            then
                sudo apt-get install xvfb
                break
            fi
        fi

    done
fi

echo "Setting file up for xvfb usage"
sed -ri 's/(xvfb_installed =).*/\1 True/g' get_xsec.py

