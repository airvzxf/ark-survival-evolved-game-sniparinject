# To-Do's List

## General

- [ ] `ELF64` binary file in Linux.
    - [ ] Create executable file in Linux.
    - [ ] Build the executable file in the GitHub workflows.
- [ ] Core module. Extractions and refactors.
    - [ ] Create a Python packages (https://pypi.org/) for the `core` module.
        - [ ] Name of the project: `SniPar` = Sniffer and Parser.
    - [ ] Extract the core and only have the module game with the `Ark`
      classes.
    - [ ] Extract the `Mana Plus` logic and create it own repository.

## Feature

### Settings are the goodies

- [ ] Control all from settings.
    - [ ] Load settings file every iteration.
    - [ ] Create generic source code which take all the information and rules
      from the `settings.yml` file.
    - [ ] Override text format for host, node and error.
    - [ ] Documentation for the different options in settings.
        - [ ] Types: [Python Structs][structs].
        - [ ] Linux: Man page.
        - [ ] Empty struct name means unknown value.

Empty struct name means unknown value:

```yaml
struct:
  - target:
      type: unsigned int
      name: Target
  -:
  type: unsigned char
  name: This value could be none, too.
message: '--> Player action | {target} | {} |'
message_changed_order: '--> Player action | {} | {target} |'
```

[structs]: https://docs.python.org/3/library/struct.html#format-characters
