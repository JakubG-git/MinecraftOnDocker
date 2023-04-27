FROM ubuntu

# Update and install dependencies

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y \
    openjdk-8-jdk \
    screen 

RUN apt-get install -y wget 

RUN apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Download and install Minecraft

RUN mkdir -p /opt/minecraft \
    && wget -O /opt/minecraft/minecraft_server.jar https://launcher.mojang.com/v1/objects/fe123682e9cb30031eae351764f653500b7396c9/server.jar

RUN echo "eula=true" > /opt/minecraft/eula.txt

COPY startServ.sh /opt/minecraft/startServ.sh

COPY server.properties /opt/minecraft/server.properties

WORKDIR /opt/minecraft

RUN chmod +x startServ.sh

ENTRYPOINT ["./startServ.sh"]

CMD ["-x", "1024M", "-m", "512M"]

 





