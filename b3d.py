#!/usr/bin/env python3

import json
import os
import sys
import pwd
import grp

default_owner = "root"
default_group = "root"
default_mode = "644"

json_path = "/etc/b3d.json"
gpio_sysfs_path = "/sys/class/gpio/"
properties = ["edge", "direction", "value"]


def print_help():
    print("""
    Usage: gpio_b3.py command"
    start  - to export and configure all the GPIOs defined in the configuration
             file (default /etc/gpio_b3.json)
    stop   - to unexport all the GPIOs defined in the configuration file
             (default /etc/gpio_b3.json)
    reload - to export the new GPIOs and update the ownership and permissions
             of the old ones""")


def start(reload):
    with open(json_path) as gpio_json:
        gpios = json.load(gpio_json)["gpios"]

        for gpio in gpios:
            with open(gpio_sysfs_path + "export", "w") as export:
                try:
                    path_gpio = gpio_sysfs_path + "gpio" + gpio["number"] + "/"
                    exist = os.path.exists(path_gpio)

                    if reload and exist:
                        print("Updating GPIO " + gpio["number"] + " ownership and permissions... ", end="")
                    else:
                        print("Exporting and configuring GPIO " + gpio[
                              "number"] + "... ", end="")
                        print(gpio["number"], file=export)
                        export.flush()

                    uid = pwd.getpwnam(
                        gpio["owner"] if "owner" in gpio else default_owner).pw_uid
                    gid = grp.getgrnam(
                        gpio["group"] if "group" in gpio else default_group).gr_gid
                    mode = int(
                        gpio["mode"] if "mode" in gpio else default_mode, 8)

                    for property in properties:
                        os.chown(path_gpio + property, uid, gid)
                        os.chmod(path_gpio + property, mode)

                        if not (reload and exist):
                            try:
                                value = gpio[property]
                                with open(path_gpio + property, "w") as filename:
                                    print(value, file=filename)
                            except KeyError:
                                pass

                except BaseException as e:
                    print("ERROR : " + str(e))
                else:
                    print("done")


def stop():
    with open(json_path) as gpio_json:
        gpios = json.load(gpio_json)["gpios"]

        file_name = os.path.join(gpio_sysfs_path, "unexport")
        with open(file_name, "w") as unexport:
            for gpio in gpios:
                number = gpio["number"]
                try:
                    if os.path.exists(gpio_sysfs_path + "gpio" + number):
                        print("Unexporting GPIO {}...".format(number), end="")
                        print(number, file=unexport)
                        unexport.flush()
                except BaseException as e:
                    print("ERROR :", str(e))
                else:
                    print("done")


if len(sys.argv) != 2:
    print_help()
else:
    if sys.argv[1] == "start":
        start(False)
    elif sys.argv[1] == "stop":
        stop()
    elif sys.argv[1] == "reload":
        start(True)
    else:
        print_help()
