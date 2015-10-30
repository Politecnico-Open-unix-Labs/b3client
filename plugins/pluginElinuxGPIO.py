import json
import pwd
import grp
gpio_sysfs_path = "/sys/class/gpio/"
properties = ["edge", "direction", "value"]

properties = {
    #"edge"      :'non lo so',
    #"direction" :"in",
    #"direction" :"out",
    #"value"     :"0",
    #"value"     :"wooo??",
    }

default_owner="bits"
default_group="bits"
default_mode ="644"
def reg_gpio(
    gpio_properties,
    gpio_pin_number,
    owner = default_owner,
    group = default_group
    mode  = default_mode):
    with open(gpio_sysfs_path + "export", "w") as export:
        path_gpio = gpio_sysfs_path + "gpio" + gpio_pin_number + "/"
        exist = os.path.exists(path_gpio)
        #set file owner
        uid = pwd.getpwnam(gpio["owner"]).pw_uid
        #set group
        gid = grp.getgrnam(gpio["group"]).gr_gid
        mode = int(mode, 8)
        for pr in gpio_properties:
            os.chown(path_gpio + pr, uid, gid)
            os.chmod(path_gpio + pr, mode)
            if pr in gpio:
                value = gpio[pr]
                with open(path_gpio + pr, "w") as filename:
                    print(value, file=filename)
def setup():

    pass

def handle(data):
    pass
