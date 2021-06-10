# ARK Game

Intercept and read the network packages to find information about the game, but
it could be useful for any network sniffer. This project is work in progress.
Reefer to the [To-Do's][todo] list to check what is done and what is coming.

## Usage

I will create a Docker image to generate the executable binary file (ELF64).

Right now, I recommend checking the file `./src/requirements.txt` and install
all the packages, but the only two special Python's packages that you need
are `scapy` and `PyYAML`.

Modify the settings located in the file `./src/settings.yml`. It needs to set
the network interface which could get by the command `ip addr` or
`ls -1 /sys/class/net`, the next two are the host IP and its port. In our case
we will use the game IP and port, you could use this command to get the
information `sudo netstat -nap | grep -i NAME_OF_GAME_PROCESS`. If not found
the game, run the command `lsof -i` to show all the process which has
connection to the network, check the column `NAME` to review the connection
`manaplus   5563 wolf ... MSIGT73EVR7RF:55238->52.174.196.146:5122
(ESTABLISHED)`.

Execute the application:

```bash
# Go to the source code
cd src

# Execute with root permissions the main script
sudo python3 main.py
```

### Example

It is for the game `Mana Plus`, but it is helpful in the middle time that I
finish the modules for `Ark Evolve`.

[![asciicast][ascii-mana-image]][ascii-mana-link]

## Parse of Packages

Increase the parsing of the packages are available for everyone, that you need
is `git clone` this repository and then go to the directory
`./src/game/mana_plus` which has two important files: `host.py` and `node. py`.
The host is handling the packages coming from the server.

### Steps:

Add an action:

```python
def __init__(self, raw_data: bytes):
    self.actions = {
        0x78: self._npc_info,
        0x87: self._player_move,
        0x8a: self._fight,
        0xff: self._NEW_FUNCTION,  # Add here your function. ID package 
        # usually is an unsigned short integer with 2 bytes with max size
        # of 0xffff.
    }
```

Create the new function:

```python
def _NEW_FUNCTION(self) -> str:
    monster_id, unknown_1 = unpack('<Ic', self._get_data(5))
    monster_id = hex(monster_id).zfill(10)
    unknown_1 = unknown_1.hex()

    message = self.text_format('<-- NEW FUNCTION', TextStyle.TITLE)
    message += self.text_format(' |')
    message += self.text_format(' ID', TextStyle.BOLD)
    message += self.text_format(f' {monster_id}', TextStyle.LIGHT)
    message += self.text_format(' |')
    message += self.text_format(' Unknown', TextStyle.BOLD)
    message += self.text_format(f' {unknown_1}', TextStyle.LIGHT)
    # The output for the message variable is:
    # <-- NEW FUNCTION | ID 0xf03614ab | Unknown 1f

    return message
```

All the data coming from the network or server usually is big-endian, to read
this as the game interpretation needs to convert to little-endian. In this
example if you receive a raw data `ff 00 ab 14 36 f0 1f`. The parse should be:

- ID Action package: `ff 00` = `0x00ff` = `255`.
- ID Monster: `ab 14 36 f0` = `0xf03614ab`.
- Unknown: `1f` = `0x1f` = `31`.

Enjoy!


[todo]: ./TODO.md

[ascii-mana-image]: https://asciinema.org/a/R0mxcmrpWHzX96NDJyc7kyTDB.svg

[ascii-mana-link]: https://asciinema.org/a/R0mxcmrpWHzX96NDJyc7kyTDB
