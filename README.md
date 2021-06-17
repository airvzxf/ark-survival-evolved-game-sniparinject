# ARK: Survival Evolved Game

Intercept and read the network packets to find information about the game, but
it could be useful for any network sniffer. This project is work in progress.
Reefer to the [To-Do's][todo] list to check what is done and what is coming.

## Run it

### Locally

For more information go to the [sniparinject page in PyPi][sniparinject-pypi].

```bash
python3 -m pip install sniparinject
git clone https://github.com/airvzxf/ark-survival-evolved-game-network-packet-sniffer.git
cd ark-survival-evolved-game-network-packet-sniffer || exit 123
cd src || exit 123
# Make modification to the source code files: main.py and settings.yml.
# Run your changes.
sudo python3 main.py
```

### As a developer

The only special Python's packages that you need is `sniparinject`. The
suggested version of `Python` is `>= 3.9`. Follow the commands to set up and
install this package.

```bash
git clone https://github.com/airvzxf/ark-survival-evolved-game-network-packet-sniffer.git
cd ark-survival-evolved-game-network-packet-sniffer || exit 123
./src/script/setup-dev.bash
```

After this setup, it could be easy to activate the vEnv and start to work.

```bash
# Inside of the GitHub cloned directory.
cd src || exit 123
source ./venv/bin/activate
# Make modification to the source code files (main.py and settings.yml).
# Run your changes.
sudo python3 main.py
# Finally deactivate the vEnv.
deactivate
```

## Usage

The settings, needs to set the network interface which could get by the
command `ip addr` or `ls -1 /sys/class/net`. The next two are the host IP and
its port, in our case we will use the game IP and port. You could use this
command `lsof -i` to show all the process which has connection to the network,
check the column `NAME` to review the connection
`manaplus   5563 wolf ... MSIGT73EVR7RF:55238->52.174.196.146:5122
(ESTABLISHED)`. Also, another command is
`sudo netstat -nap | grep -i NAME_OF_GAME_PROCESS`.

`./src/settings.yml`

```yaml
Network:
  interface: enp4s0

Server:
  host: 52.174.196.146
  port: 5122
```

Execute the application:

```bash
# Go to the source code directory.
cd src
# Execute with root permissions the main script.
sudo python3 main.py
```

### Example

It is for the game `Mana Plus`, but it is helpful in the middle time that I
finish the modules for `ARK: Survival Evolved`.

[![asciicast][ascii-mana-image]][ascii-mana-link]

## Settings

Looking for add, modify or remove parse rules. It does not need to modify any
file in the source code. It has the `./src/settings.yml` file which is able to
add, modify or remove any rule, please reefer to the file in this project to
understand in deep.

The settings file is little complex, the better documentation is in the
`sniparinject` [official read me file][sniparinject-github].

Enjoy!


[todo]: ./TODO.md

[sniparinject-pypi]: https://pypi.org/project/sniparinject/

[ascii-mana-image]: https://asciinema.org/a/R0mxcmrpWHzX96NDJyc7kyTDB.svg

[ascii-mana-link]: https://asciinema.org/a/R0mxcmrpWHzX96NDJyc7kyTDB

[sniparinject-github]: https://github.com/airvzxf/sniparinject/blob/main/README.md#settings
