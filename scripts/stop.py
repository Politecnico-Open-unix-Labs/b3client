#!/usr/bin/env python3

import os
import re

gpio_sysfs_path = "/sys/class/gpio/"

dir_content = " ".join(os.listdir(gpio_sysfs_path))
gpios = re.findall("gpio([0-9]+)", dir_content)

with open(gpio_sysfs_path + "unexport", "w") as unexport:
	for gpio in gpios:
		print("Unexporting gpio " + gpio + "... ", end="")
		print(gpio, file=unexport)
		unexport.flush()
		print("done")

