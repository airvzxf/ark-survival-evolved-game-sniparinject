# To-Do's List

## General

- [ ] `ELF64` binary file in Linux.
    - [ ] Create executable file in Linux.
    - [ ] Build the executable file in the GitHub workflows.
- [ ] Core module. Extractions and refactors.
    - [ ] Create a Python packages (https://pypi.org/) for the `core` module.
        - [ ] Name of the project: `SniPar Inject` = Sniffer, Parser and
          Inject.
        - [ ] Documentation for the different options in settings.
            - [ ] Types: [Python Structs][structs].
            - [ ] Linux: Man page.
    - [ ] Extract the core and only have the module game with the `Ark`
      classes.
    - [ ] Extract the `Mana Plus` logic and create it own repository.

## Feature

### Settings are the goodies

- [x] Control all from settings.
    - [x] Load settings file every iteration.
    - [x] Create generic source code which take all the information and rules
      from the `settings.yml` file.
    - [x] Override text for host, node and error.

[structs]: https://docs.python.org/3/library/struct.html#format-characters
