# b3d

Deamon client of [b3api](https://github.com/Politecnico-Open-unix-Labs/b3api)
and host for python plugins.

## Details

- Load the plugins as modules from the plugins folder
- Open a websocket connection to the server and wait for the json state
- Each plugin subscribe for a specific section of the json (`name` field)
- The current state and any successive update are set to plugis calling the
  `handle` method
- Plugins can also send information to the server


## TODO

- `read_button_from_GPIO` plugin (RasberryPi only)
- `temperature` plugin
- `setup.py` and deploy script
