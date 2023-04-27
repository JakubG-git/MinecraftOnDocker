FROM ubuntu

# Update and install dependencies

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y \
    openjdk-19-jre-headless \
    screen 

RUN apt-get install -y wget 

RUN apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Download and install Minecraft

RUN mkdir -p /opt/minecraft \
    && wget -O /opt/minecraft/minecraft_server.jar https://piston-data.mojang.com/v1/objects/8f3112a1049751cc472ec13e397eade5336ca7ae/server.jar

RUN echo "eula=true" > /opt/minecraft/eula.txt

COPY scripts/startServ.sh /opt/minecraft/startServ.sh

COPY files/server.properties.default /opt/minecraft/server.properties

WORKDIR /opt/minecraft

RUN chmod +x startServ.sh

ENTRYPOINT ["./startServ.sh"]

CMD ["-x", "1024M", "-m", "512M"]

 





