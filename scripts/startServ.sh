#!/bin/bash

version="1.0"

display_default_settings(){
    echo "java -Xmx1024M -Xms1024M -jar minecraft_server.jar nogui"
}

default_settings(){
    echo "Starting server with default settings..."
    display_default_settings
    java -Xmx1024M -Xms1024M -jar minecraft_server.jar nogui
}

help(){
    echo "Usage: startServ.sh [OPTION]..."
    echo "Starts the Minecraft server."
    echo ""
    echo "  -h, --help      display this help and exit"
    echo "  -v, --version   output version information and exit"
    echo "  -j, --jar       specify the jar file to run"
    echo "  -x, --xmx       specify the maximum memory allocation pool for a Java Virtual Machine (JVM)"
    echo "  -m, --xms       specify the initial memory allocation pool for a Java Virtual Machine (JVM)"
    echo ""
    echo "If no arguments are passed, the server will start with default settings."
    display_default_settings
}

if [ "$#" -eq 0 ]; then
    default_settings
else
    jar="minecraft_server.jar"
    xms="1024M"
    xmx="1024M"
    while [ "$#" -gt 0 ]; do
        case "$1" in
          -h|--help)
            help
            exit 0
            ;;
          -v|--version)
            echo "startServ.sh version $version"
            exit 0
            ;;
          -j|--jar)
            jar="$2"
            shift 2
            ;;
          -x|--xmx)
            xmx="$2"
            shift 2
            ;;
          -m|--xms)
            xms="$2"
            shift 2
            ;;
          *)
            echo "Invalid argument: $1"
            echo "Try 'startServ.sh -h, --help' for more information."
            exit 1
            ;;
        esac
    done
    echo "Starting server with the following settings..."
    echo "java -Xmx${xmx} -Xms${xms} -jar ${jar} nogui"
    java -Xmx${xmx} -Xms${xms} -jar ${jar} nogui
fi