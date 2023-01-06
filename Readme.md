# Advent of Code

A project to solve the
[advent of code](https://adventofcode.com)
problems with various programming languages.

## Command Line Execution

### C/C++

```sh
clang answers.c && ./a.out < input.txt && rm a.out
```

### C# (dotnet)

The dotnet build system is complicated.  See <https://stackoverflow.com/a/56133028/542911>.
A script based on that approach has been created.  This script may require tweaking if there
are changes to the dotnet build system, but it should work with different versions of dotnet.

```sh
../run_dotnet.sh answers input.txt
```

### C# (mono)

Mono is not yet (Jan 2023) providing an ARM based build, so installation requires
rosetta on newer Apple silicon.  I am not testing mono on Apple Silicon until there
is an ARM based build.

```sh
csc answers.cs && mono answers.exe < input.txt && rm answers.exe
```

### dart

```sh
dart run answers.dart < input.txt
```

### Go

```sh
go run answers.go < input.txt
```

### Haskell

```sh
ghc answers.hs && ./answers < input.txt && rm answers answers.hi answers.o
```

### Java

```sh
java answers.java < input.txt
```

### Javascript (browser)

TBD

### Javascript (node)

```sh
node answers.js < input.txt
```

### Julia

```sh
julia answers.jl < input.txt
```

### Python

```sh
python answers.py < input.txt
```

### Rust

```sh
rustc answers.rs && ./answers < input.txt && rm answers
```

### Swift

```sh
swiftc answers.swift && ./answers < input.txt && rm answers
```

### Typescript

TBD

### Run All

To test all solutions in a folder.

```sh
cd 2015-01
../runall.sh
```

### Project based approach

#### C# DotNet

```sh
dotnet new console -o dotnetAOC; cd dotnetAOC
cp template.cs y2020d02.cs
code . # edit Program.cs and y2020d02.cs
dotnet run 2020-02 < ../2020-02/input.txt
```

#### Rust Project

See <https://github.com/rsarwas/learn-rust>

#### Swift Project

See `swiftAOC\Readme.md` for details of a swift solution to solve all puzzles
with a framework or package based approach.

## Installing and updating Languages

Instructions are only for MacOS and may become out of date as the
various development kits evolve.

Several installs assume you have _Homebrew_ installed.
Homebrew requires the XCode command line tools (See Clang/Swift install).
See <https://docs.brew.sh/Installation>

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## C Lang

* Install XCode from the AppStore
* Open XCode and "yes" to install additional tools
* or run `xcode-select --install`
* Check in XCode Preferences -> locations, that the command line tools
  have a valid path.
* After updating XCode, run `xcode-select --install` and check Xcode preferences

## dart/flutter

* flutter includes dart
* <https://flutter.dev/docs/get-started/install>
  
```sh
cd ~/MyRepos
git clone https://github.com/flutter/flutter.git -b stable
# write ~/MyRepos/flutter/bin to /etc/paths.d/flutter
# or add to the path in .profile
flutter precache
flutter doctor
```

* Updating, pull from repo and rebuild (`flutter precache`)

## DotNet

* <https://dotnet.microsoft.com/download>
* Install and updates are easiest with "Installer" download.
* Installer puts files in `/usr/local/share/dotnet` and `/etc/paths.d`
* Updating: Check version `dotnet --version` against website, and add newer versions.
* After the initial install, tarballs can be downloaded and unpacked
  below the dotnet install location.

## Glasgow Haskell Compiler (GHC)

* <https://www.haskell.org/ghcup/>
* `curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh`
* Ghcup installs files in `~/.ghcup` and modifies your shell setup file.
  (`~/.config/fish/config.fish` or `~/.zenv`, or `~/.profile`)
* Update with `ghcup tui`

## Go Lang

* <https://golang.org/dl>
* Download the installer package;
* Installer puts files in `/usr/local/go`, `~/go`, and `/etc/paths.d`
* Updating: Check version `go version` against website, and reinstall.

## Java Install/Update

* See <https://openjdk.org/>
* Download and unpack the latest tar ball into a `/usr/local/share/java`
* Edit yous shell environment:
  * Assign `/usr/local/share/java/jdk-19.0.1.jdk/Contents/Home` to the `JAVA_HOME`
    environment variable (adjust version number as necessary)
  * Add `$JAVA_HOME/bin` to `PATH` environment variable
* Updating: Check version `java --version` against website, and add newer version.

## Julia Lang

* <https://julialang.org/downloads/>
* Running the installation package installs julia into `/Applications`
* link to `~/bin` with  `ln -s /Applications/Julia-1.8.app/Contents/Resources/julia/bin/julia ~/bin`
* Adding alias to `~/.profile` or `~/.config/fish/config.fish` is good, but they are not
  available in a script.
* Updating: Check version `julia --version` against website, and reinstall.

## Mono

* `mono --version`
* <https://www.mono-project.com/download/stable/#download-mac>
* Mono requires rosetta on Apple Silicon as of version 6.12.0 Stable (Jan 2023)
* Updating: Check version `mono --version` against website, and reinstall.

## Node

* If installing typescript, `yarn` installs `node` as a dependency
* Otherwise `brew install node`

## Python Install

* `brew install pyenv`
* configure pyenv and install python per https://github.com/pyenv/pyenv

## Rust Lang

* <https://www.rust-lang.org/tools/install>
* `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
* Installs files in `~/.rustup` and `~/.cargo`
* Add `$HOME/.cargo/bin` to your PATH
* Update with `rustup update`

## Swift Install

Installs with XCode command line tools. See Clang above

## Typescript Install

* `brew install yarn`
* `yarn global install typescript`
