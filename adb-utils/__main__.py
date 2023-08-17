#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--serial", help="device serial number")
    parser.add_argument("-V", "--server-version", action="store_true", help="show adb server version")
    parser.add_argument("-l", "--list", action="store_true", help="list devices")
    parser.add_argument("-i", "--install", help="install from local apk or url")
    parser.add_argument("--install-confirm", action="store_true",
                        help="auto confirm when install (based on uiautomator2")
    parser.add_argument("-u", "--uninstall", help="uninstall apk")
    parser.add_argument("-L", "--launch", action="store_true", help="launch after install")
    parser.add_argument("--qrcode", help="show qrcode of the specified file")
    parser.add_argument("--parse", type=str, help="parse package info from local file or url")
    parser.add_argument("--clear", action="store_true", help="clear all data when uninstall")
    parser.add_argument("--list-packages", action="store_true", help="list packages installed")
    parser.add_argument("--current", action="store_true", help="show current package info")
    parser.add_argument("-p", "--package", help="show package info in json format")
    parser.add_argument("--grep", help="filter matched package names")
    parser.add_argument("--connect", type=str, help="connect remote device")
    parser.add_argument("--shell", action="store_true", help="run shell command")
    parser.add_argument("--minicap", action="store_true", help="install minicap and minitouch to device")
    parser.add_argument("--screenshot", type=str, help="take screenshots")
    parser.add_argument("-b", "--browser", help="open browser in device")
    parser.add_argument("--push", help="push local file to remote")
    parser.add_argument("--pull", help="pull device file to local")
    parser.add_argument("--dump-info", action="store_true", help="dump info for dev")
    parser.add_argument("--track", action="store_true", help="trace device status")
    parser.add_argument("args", nargs="*", help="arguments")

    args = parser.parse_args()
    print(args.serial)
    print(args.server_version)


if __name__ == "__main__":
    main()
