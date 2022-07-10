import subprocess
from pathlib import Path
from typing import Union, Dict
from pytest import mark

from pretty_popen.popen import PrettyPopen

artefact = Path(__file__).parents[2].absolute().joinpath("tests",
                                                         "unit",
                                                         "artefacts")

blank = {
    'python3 tests/unit/artefacts/command.py': [
        ['--arg_one', 1],
        ['--arg_two', 2],
        ['--arg_three']]
}
args_json = artefact.joinpath("command.json").as_posix()
args_yaml = artefact.joinpath("command.yaml").as_posix()


def test_content_json():
    assert PrettyPopen.read_json(args_json) == blank


@mark.skip
def test_content_yaml():
    assert PrettyPopen.read_yaml(args_yaml) == blank


def func(cmd: Union[Dict, str]):
    popen = PrettyPopen(cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        shell=True)
    stdout, stderr = popen.communicate()
    stderr = stderr.decode('utf-8')
    stdout = stdout.decode('utf-8').split('\n')
    assert stdout == ['1', '2', 'arg_three', '']
    assert stderr == ""


def test_str():
    return func(cmd=f"python3 {artefact.joinpath('command.py').as_posix()} --arg_one 1 --arg_two 2 --arg_three")


def test_dict1():
    return func(cmd=blank)


def test_dict2():
    return func(cmd={f"python3 {artefact.joinpath('command.py').as_posix()}": [("--arg_one", 1),
                                                                               ("--arg_two", 2),
                                                                               ("--arg_three",)]})


@mark.skip
def test_yaml():
    return func(cmd=args_yaml)


def test_json():
    return func(cmd=args_json)
