# Passive Aggressor

This project provides a simple Python-based tool to compress files into ridiculously deep nested directories
where the path can also spell out a custom message.

This is perfect for those peers you don't like.

**This currently only works on Linux but support for Windows and Mac has been started in the code base.**

## TL;DR - Linux

To get started quickly with a simple deployment, execute the following `bash` commands on a *nix based system
with `git` installed:

```
git clone https://github.com/AzorianSolutions/passive-aggressor.git
cd passive-aggressor
./deploy/bare-metal/linux/debian.sh
source venv/bin/activate
aggressor -m "Your message here" ./path/to/output/file.zip ./path1/to/files/to/compress ./path2/etc
```

## Options & Arguments

### Debug Mode

You can activate debug mode with the `-d` or `--debug` flag. This will cause the program to print out a lot of
information.

```
aggressor -d ./path/to/output/file.zip ./path/to/files/to/compress/*
```

### Message Option

You can optionally specify a custom message with the `-m` or `--message` flag. This will cause the program to implant
the message within the middle of the randomized directory structure, with each character becoming its own directory.

```
aggressor -m "Your message here" ./path/to/output/file.zip ./path/to/files/to/compress/*
```

If your message is "Hello World", the directory structure in the archive will look something like this,
except much longer!

```
a/F/d/r/W/5/v/1//H/e/l/l/o/W/o/r/l/d/f/0/3/J/d
```

### Output File Argument

You must specify the output file with the first argument. The file name must end with either `.zip` or `.tar.gz`.

```
aggressor OUTPUT_PATH_HERE ./path/to/files/to/compress/*
```

### Input Path(s) Argument(s)

You must specify at least one input file or directory with the second argument. You can specify multiple files and
directories.

```
aggressor ./path/to/output/file.zip INPUT_PATH_1 INPUT_PATH_2 INPUT_PATH_3
```
