# MinecraftOnDocker
## Usage
### Build
```bash
docker compose build
```
### Run
```bash
./chooseOpts.py
```
or
```bash
python3 chooseOpts.py
```

## Options
### startServ.sh
```
Usage: startServ.sh [OPTION]...
Starts the Minecraft server.

  -h, --help      display this help and exit
  -v, --version   output version information and exit
  -j, --jar       specify the jar file to run
  -x, --xmx       specify the maximum memory allocation pool for a Java Virtual Machine (JVM)
  -m, --xms       specify the initial memory allocation pool for a Java Virtual Machine (JVM)

If no arguments are passed, the server will start with default settings.
```
### chooseOpts.py
```
Usage: python chooseOpts.py [options]
    Options:
        -h, --help: Show this help message.
        -s, --start: Start the server.
        -q, --quit: Stop the server.
        -o, --options: Configure the server properties.
        -c, --console: Open the server console.
If no options are specified, the server will be started.
```