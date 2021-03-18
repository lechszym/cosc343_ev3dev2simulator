"""
Main module of the ev3dev2simulator. Starts the server thread listening for incoming connections and
starts the simulator itself. The simulator and server threads are started based on the arguments given.
"""

import argparse
import sys
import os

from ev3dev2simulator.config.config import load_config, get_world_config
from ev3dev2simulator.visualisation.visualiser import Visualiser
from ev3dev2simulator.connection.server_sockets import ServerSockets
from ev3dev2simulator.state.world_simulator import WorldSimulator
from ev3dev2simulator.state.world_state import WorldState
from ev3dev2simulator import version as sim_version
from ev3dev2 import version as api_version


def parse_args(args):
    """
    Parses the arguments given to the program. Mainly arguments for the visualisation.
    :param args: list of parameters given to program
    :return: list of parsed values based on parameters
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-V", "--version",
                        action='store_true',
                        help="Show version info")
    parser.add_argument("-t", "--simulation_file",
                        default='config_small',
                        help="Path to the configuration file. Defaults to config_small",
                        required=False,
                        type=str)
    parser.add_argument("-2", "--show-on-second-monitor",
                        action='store_true',
                        help="Show simulator window on second monitor instead, default is first monitor")
    parser.add_argument("-f", "--fullscreen",
                        action='store_true',
                        help="Show simulator fullscreen")
    parser.add_argument("-m", "--maximized",
                        action='store_true',
                        help="Show simulator maximized")
    return parser.parse_args(args)


def main(orig_path):
    """
    Spawns the user thread and creates and starts the simulation.
    """
    args = vars(parse_args(sys.argv[1:]))

    if args['version']:
        print("version ev3dev2           : " + api_version.__version__)
        print("version ev3dev2simulator  : " + sim_version.__version__)
        sys.exit(0)

    use_second_screen_to_show_simulator = args['show_on_second_monitor']
    show_fullscreen = args['fullscreen']
    show_maximized = args['maximized']

    load_config(args['simulation_file'], orig_path)

    config = get_world_config()

    cosc343tiles = False
    for i in range(len(config['obstacles'])):
        if 'type' in config['obstacles'][i] and config['obstacles'][i]['type'] == 'tiles':
            del config['obstacles'][i]
            cosc343tiles = True
            break

    if cosc343tiles:
        grout_size = 3
        small_tile_size = 33
        large_tile_size = 3 * small_tile_size

        n_large_tiles_horiz = 12
        n_large_tiles_ver = 9

        tot_width = n_large_tiles_ver * large_tile_size + (n_large_tiles_ver + 1) * grout_size
        tot_height = n_large_tiles_ver * (2 * grout_size + large_tile_size) + (n_large_tiles_ver - 1) * small_tile_size

        hscale = config['board_width'] / tot_width
        vscale = config['board_height'] / tot_height

        scale = min(hscale, vscale)
        if scale < 1:
            scale = 1

        grout_colour = (100, 100, 100)
        large_tile_colour = (240, 240, 240)
        black_tile_colour = (1, 1, 1)
        white_tile_colour = (254, 254, 254)

        grout_size = int(grout_size * scale)
        small_tile_size = int(small_tile_size * scale)

        large_tile_size = 3 * small_tile_size

        x = 1
        x = x * (large_tile_size + grout_size) + large_tile_size / 2
        start_tile_x = int(x)

        y = 7
        y = y * (large_tile_size + 2 * grout_size) + (y - 1) * small_tile_size + large_tile_size / 1.2
        start_tile_y = int(y)

        start_tile = {'name': 'stile1',
                 'x': int(start_tile_x),
                 'y': int(start_tile_y),
                 'width': int(large_tile_size*0.6),
                 'height': int(large_tile_size*0.8),
                 'color': black_tile_colour,
                 'type': 'tile'

                 }
        config['obstacles'].append(start_tile)

        for i in range(len(config['obstacles'])):
            if 'tile' in config['obstacles'][i]:
                t = config['obstacles'][i]['tile']
                x = 8 + (t - 1) % 3
                y = 1 + int((12 - t) / 3)
                config['obstacles'][i]['x'] = int(x * (large_tile_size + grout_size) + grout_size + large_tile_size / 2)
                config['obstacles'][i]['y'] = int(
                    y * (large_tile_size + 2 * grout_size) + (y) * small_tile_size + large_tile_size / 2)
            if 'radius' in config['obstacles'][i]:
                config['obstacles'][i]['radius'] *= scale

        # Vertical grouts
        grout_length = n_large_tiles_ver * (large_tile_size + 2 * grout_size) + (n_large_tiles_ver) * small_tile_size
        for i in range(n_large_tiles_horiz + 1):
            x = i * (large_tile_size + grout_size)
            y = 0

            grout = {'name': 'gv%d' % i,
                     'x': int(x + grout_size / 2),
                     'y': int(y + grout_length / 2),
                     'width': grout_size,
                     'height': grout_length,
                     'color': grout_colour,
                     'type': 'tile'

                     }
            # x += grout_size/2
            # y += grout_length/2
            config['obstacles'].append(grout)

        # Horizontal grouts
        grout_length = n_large_tiles_horiz * large_tile_size + (n_large_tiles_horiz + 1) * grout_size
        y = 0
        for i in range(2 * n_large_tiles_ver):
            x = 0
            # y = i*(large_tile_size+grout_size)
            # y = 0

            grout = {'name': 'gh%d' % i,
                     'x': int(x + grout_length / 2),
                     'y': int(y + grout_size / 2),
                     'width': grout_length,
                     'height': grout_size,
                     'color': grout_colour,
                     'type': 'tile'
                     }
            if i % 2 == 0:
                y += large_tile_size + grout_size
            else:
                y += small_tile_size + grout_size

            # x += grout_size/2
            # y += grout_length/2
            config['obstacles'].append(grout)

        # Large tiles
        k = 0
        for i in range(n_large_tiles_horiz):
            for j in range(n_large_tiles_ver):
                x = i * large_tile_size + (i + 1) * grout_size
                y = grout_size + j * large_tile_size + 2 * j * grout_size + j * small_tile_size
                tile = {'name': 'lt%d' % k,
                        'x': int(x + large_tile_size / 2),
                        'y': int(y + large_tile_size / 2),
                        'width': large_tile_size,
                        'height': large_tile_size,
                        'color': large_tile_colour,
                        'type': 'tile'
                        }

                k += 1
                config['obstacles'].append(tile)

        # Small tiles
        k = 0
        for i in range(n_large_tiles_ver):
            y = (i + 1) * large_tile_size + (i + 1) * 2 * grout_size + i * small_tile_size
            for j in range(n_large_tiles_horiz * 3):
                x = j * small_tile_size + (int(j / 3) + 1) * grout_size
                if j % 2 == 0:
                    colour = black_tile_colour
                else:
                    colour = white_tile_colour

                tile = {'name': 'st%d' % k,
                        'x': int(x + small_tile_size / 2),
                        'y': int(y + small_tile_size / 2),
                        'width': small_tile_size,
                        'height': small_tile_size,
                        'color': colour,
                        'type': 'tile'
                        }

                k += 1
                config['obstacles'].append(tile)

        start_tile['name'] = 'stile2'
        config['obstacles'].append(start_tile)


        x = config['robots'][0]['center_x']
        x = x * (large_tile_size + grout_size) + large_tile_size / 2
        config['robots'][0]['center_x'] = int(x)

        y = config['robots'][0]['center_y']
        y = y * (large_tile_size + 2 * grout_size) + (y - 1) * small_tile_size + large_tile_size / 1.2
        config['robots'][0]['center_y'] = int(y)

    world_state = WorldState(config)

    world_simulator = WorldSimulator(world_state)

    visualiser = Visualiser(world_simulator.update, world_state, show_fullscreen, show_maximized,
                            use_second_screen_to_show_simulator)

    server_thread = ServerSockets(world_simulator)
    server_thread.setDaemon(True)
    server_thread.start()

    visualiser.run()


if __name__ == '__main__':
    _ORIG_PATH = os.getcwd()
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    os.chdir(SCRIPT_DIR)
    main(_ORIG_PATH)
