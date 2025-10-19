# Car

Car is a package manager for Redrose Linux. It will also become a wrapper for other package managers to simplify package management.

## Roadmap
- [x] Basic functionality
- [x] Basic versioning
- [ ] More advanced versioning
- [x] Mirrors
- [ ] Website with all packages from official repos
- [ ] .car tarballs so installation is not only online
    - [ ] if the package argument of get ends with .car, install locally

## Syntax

```bash
car get|delete|update

# Examples
car get <package> [--noconfirm]
car delete <package>
car update
```

- `get <package> [--noconfirm]` - install a package. Use `--noconfirm` to skip prompts.
- `delete <package>` - remove a package.
- `update` - update all packages. *(currently not functional)*

## Creating hooks
1. Add the file to your .config/car/post-inst-hooks file
2. create the file

## Making repos
1. open .config/mirrors.car
2. add something similar to this:
```
:base:
install_script = https://raw.githubusercontent.com/crust-project/car-binary-storage/main/
packagelist = https://raw.githubusercontent.com/crust-project/car/main/existing-packages.txt
:end:
```

## Creating packages

Start by creating a file named `install_script`.

### Version

```python
version = "0.0.1"
```

### Hooks and functions

#### beforeinst()

Optional hook that runs before installation.

```python
def beforeinst():
    print("This runs before installation!")
    print("DO NOT USE THIS FOR DEPENDENCIES")
```

#### deps()

Declare dependencies. If none, print the exact line below.

```python
def deps():
    print(":: No dependencies required")
```

#### build()

Provide build steps. If no build is required print:

```python
print(":: No build required")
```

#### install()

If the installation is not done in build(), do it here. You do not need to print no deps required, because installing (moving to /usr/bin/) does not take long. 

#### postinst()

Runs after installation. Place final install steps here if needed.

## Submitting packages

1. Fork the `car-binary-storage` repository.
2. In GitHub web UI click **New file** then **Create new file**.
3. Choose a package name. Naming rules:
   - Use `-bin` for packages that download binaries.
   - Use suffixes like `-nightly` or `-stable` for specific build channels.
   - Use `-git` if the package builds from source.
   - No suffix for a standard package.
4. Create a directory with the package name and add a file named `install_script`.
5. Paste your `install_script` content.
6. Submit a pull request. Wait for review and merge.
