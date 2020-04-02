# lopu - LOg Parsing Utility

lopu is a Python CLI application that helps you parse log files of various
kinds.

![testing](https://github.com/pvital/lopu/workflows/testing/badge.svg)

```
Usage: ./lopu.py [OPTION]... [FILE]
    -h, --help          Print help
    -f, --first=NUM     Print first NUM lines
    -l, --last=NUM      Print last NUM lines
    -t, --timestamps    Print lines that contain a timestamp in HH:MM:SS format
    -i, --ipv4          Print lines that contain an IPv4 address, matching IPs
                        are highlighted
    -I, --ipv6          Print lines that contain an IPv6 address (standard
                        notation), matching IPs are highlighted
```

If FILE is omitted, standard input is used instead.

If multiple options are used at once, the result is the intersection of their
results.

## Example supported usage:

```
./lopu.py -h
<prints help>

cat test_0.log | ./lopu.py --first 10
<prints the first 10 lines of test_0.log>

./lopu.py -l 5 test_1.log
<prints the last 5 lines of test_1.log>

./lopus.py --timestamps test_2.log
<prints any lines from test_2.log that contain a timestamp>

./lopu.py --ipv4 test_3.log
<prints any lines from test_3.log that contain an IPv4 address>

./lopu.py --ipv6 test_4.log
<prints any lines from test_4.log that contain an IPv6 address>

./lopu.py --ipv4 --last 50 test_5.log
<prints any of the last 50 lines from test_5.log that contain an IPv4 address>
```

## Testcases

To execute our suite of unit tests, execute the following command:

```
python3 -m unittest tests/test_util.py
```
