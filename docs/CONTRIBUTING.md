# Contributing

❤ Contributions of this project are always welcome!

Hi, all. I don't have a lot to say because this is a `Pre-alpha` version. I'll
update this document when this application releases on version 3.x.x or 5.x.x,
other option is if the community grow up then this document will be necessary.

## GitHub steps

Follow this simple steps to start the adventure:

- [Create a GitHub issue first][new-issue] for new features, changes, bugs,
  doubts, questions or issues.

- Do you want to get your hands dirty? Fork the main branch of the project,
  create a new branch, hack your changes and create a pull request.
    - [Fork a repo][fork-a-repo].
    - [Make a pull request][about-pull-requests].
    - [General information][contribute-github].

- Check the [Read Me file][read-me] and the [To-Do's list][to-do] to get more
  familiar with the project idea, and structure.

- Optional, we can have a Google meeting to discuss the changes, also we can
  share the screen.

## Versioning and releases

- Version nomenclature `v1.2.20210809.9ee26d8`, this is the description for
  each `vMajorVersion.MinorVersion.Date.CommitID`.
- Each developer works on his own fork.
- Create a merge request directly to `main` branch.
- If this project grows, I'll create the branches `dev` -> `beta` ->
  `main`.

## Contact

It will be a good idea to create a Slack channel or use other platform, but
this project is very small. My personal email is `israel.alberto.rv@gmail.com`.

## Build the application

For developers, it has two options for build the code: Docker or locally.

### Docker

This section is coming soon.

### Local

The only special Python's packages that you need is `sniparinject`. The
suggested version of `Python` is `>= 3.9`. Follow the commands to set up and
install this package.

```bash
git clone https://github.com/airvzxf/ark-survival-evolved-game-sniparinject.git
cd ark-survival-evolved-game-sniparinject || exit 123
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

[new-issue]: https://github.com/airvzxf/bose-connect-app-linux/issues/new

[fork-a-repo]: https://help.github.com/articles/fork-a-repo/

[about-pull-requests]: https://help.github.com/articles/about-pull-requests/

[contribute-github]: https://docs.github.com/en/github/collaborating-with-pull-requests

[read-me]: ../README.md

[to-do]: ../TODO.md
