# mariner-dev-tools
Tool to remotely query the Mariner archive database about packages

## Support
| Mariner   | x86_64 | aarch64 | debuginfo |
| ----------| -------| --------| ----------|
| 1.0       |   X    |    X    |     X     |
| 2.0       |   X    |    X    |     X     |

## Demo
```
$ ./mariner-pkg-query.py shadow-utils
```

| Mariner |     Name     |       DebugInfo        |  Version  |   Arch  |  Repo  |
|---------|--------------|------------------------|-----------|---------|--------|
|   1.0   | shadow-utils | shadow-utils-debuginfo | 4.9-8.cm1 |  x86_64 | update |
|   1.0   | shadow-utils | shadow-utils-debuginfo | 4.9-8.cm1 | aarch64 | update |
|   2.0   | shadow-utils | shadow-utils-debuginfo | 4.9-9.cm2 |  x86_64 |  base  |
|   2.0   | shadow-utils | shadow-utils-debuginfo | 4.9-9.cm2 | aarch64 |  base  |

## Todo list
* Ignore case for package with upper case (e.g., WALinuxAgent)
