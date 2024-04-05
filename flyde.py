#!/usr/bin/env python3
import argparse
import importlib
import logging
import os
import pprint
import sys
import yaml

from flyde.flow import FlydeFlow
from flyde.node import Component

logging.basicConfig(level=logging.INFO)

def add_folder_to_path(path: str):
    # Get the absolute path from the relative file path provided
    folder = os.path.abspath(os.path.dirname(path))
    if folder not in sys.path:
        sys.path.append(folder)

def load_yaml_file(yaml_file: str) -> dict:
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    return data

def py_path_to_module(py_path: str) -> str:
    return py_path.replace('/', '.').replace('.py', '')

def gen(path: str):
    """Generate TypeScript files for a module."""
    print(f'Generating TypeScript files for module {path}')
    module = py_path_to_module(path)
    mod = importlib.import_module(module)
    ts_file_path = path.replace('.py', '.flyde.ts')
    typescript = 'import { CodeNode } from "@flyde/core";\n\n'
    for name in mod.__dict__.keys():
        c = getattr(mod, name)
        if name != 'Component' and isinstance(c, type) and issubclass(c, Component):
            typescript += c.to_ts(name)

    print(f'Writing TypeScript to {ts_file_path}')
    with open(ts_file_path, 'w') as f:
        f.write(typescript)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="PyFlyde CLI that runs Flyde graphs and provides other useful functions.\n\nExamples:\n\n  flyde.py path/to/MyFlow.flyde # Runs a flow\n  flyde.py gen path/to/module.py # Generates TS files for visual editor",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('command', type=str, nargs='?', choices=['run', 'gen'], default='run', help='Command to run. Default is "run"')
    parser.add_argument('path', type=str, help='Path to a ".flyde" flow file to run or a Python ".py" module to generate typescript definitions for')

    args = parser.parse_args()

    if args.command == 'run':
        # Get the yaml file path from the command line argument
        yaml_file = args.path

        # Load the yaml file
        yml = load_yaml_file(yaml_file)

        # Get the absolute path from the yaml_file path and add it to the sys.path
        add_folder_to_path(yaml_file)

        if isinstance(yml, dict):
            flow = FlydeFlow.from_yaml(yml)

            if logging.getLevelName(logging.root.level) == 'DEBUG':
                print('Loaded flow:')
                pprint.pprint(flow.to_dict())

            flow.run()
            flow.stopped.wait()
        else:
            raise ValueError('Invalid YAML file')
    elif args.command == 'gen':
        add_folder_to_path(args.path)
        gen(args.path)
    else:
        raise ValueError(f'Unknown command: {args.command}')
