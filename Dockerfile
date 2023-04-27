FROM ubuntu

# Update and install dependencies

EXPOSE 25565

RUN apt-get update && apt-get install -y \
    openjdk-8-jdk \
    wget \
    git \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Download and install Minecraft

RUN mkdir -p /opt/minecraft \
    && wget -O /opt/minecraft/minecraft_server.jar https://launcher.mojang.com/v1/objects/fe123682e9cb30031eae351764f653500b7396c9/server.jar

RUN echo "eula=true" > /opt/minecraft/eula.txt

RUN echo $(ls -1 /opt/minecraft)

WORKDIR /opt/minecraft

ENTRYPOINT ["java", "-jar", "/opt/minecraft/minecraft_server.jar", "nogui"]

CMD ["-Xmx1024M", "-Xms1024M"]
 





