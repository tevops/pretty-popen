import json
import logging
from functools import singledispatchmethod
from json import JSONDecodeError
from pathlib import Path
from subprocess import Popen
from typing import Dict, Union, Iterable, List

from .constants import BREAK

logger = logging.getLogger(__file__)


class PrettyPopen(Popen):

    def __init__(self, args: Union[Dict, str], **kwargs):
        """
        Example usage:
            ::arg::  arg currently the following structure:
                    +------------------------------------------------+
                     Dict[str: List[Tuple] # for glad_translate and exiftool
                     ## e.g. {"gdal_translate": [("-co", '"COMPRESS=DEFLATE"'),
                                                 ("-co", '"BIGTIFF=YES"'), ...]

        """

        super(PrettyPopen, self).__init__(args=self.process_arg(args), **kwargs)

    @classmethod
    def is_proper_dict(cls, args: Dict) -> bool:
        proper_dict = isinstance(args, dict) and len(args) == 1
        proper_values = (len(val) < 3 for val in args.values())
        return proper_values and proper_dict

    @staticmethod
    def merge_dicts(list_of_dicts: Union[List[Dict], List]) -> Union[Dict, List]:
        """
        -- PyYAML reads a .yaml (as intended in the use case) into
            Dict[str: List[Dict]]
        -- JSON reads a .json into
            Dict[str: Dict]

        This function standardizes all of that.
        :param list_of_dicts:
        :return: the list of dicts merged into a single dict.
        """
        if isinstance(next(iter(list_of_dicts)), dict):

            logger.debug(list_of_dicts)
            merged_dicts = dict(keyval for subdict in list_of_dicts for keyval in subdict.items())
            logger.debug(merged_dicts)
            return merged_dicts
        return list_of_dicts

    @classmethod
    def read_yaml(cls, file_path: str):
        # with open(file_path, 'r') as stream:
        #     try:
        #         content = yaml.safe_load(stream)
        #         return {key: cls.merge_dicts(value) for key, value in content.items()}
        #     except yaml.YAMLError as exc:
        #         logger.exception(exc)
        #         raise exc
        raise NotImplementedError

    @staticmethod
    def read_json(file_path: Union[str, bytes]):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)

        except JSONDecodeError as exc:
            logger.exception(exc)
            raise exc

    def read_file(self, file: Path) -> Dict:
        """
        Args:
            :param file: Path to config file. e.g. ndvi_[something something].yaml
            :return: dict - the content of the file
        """
        logger.info(f"Reading subprocess command and arguments from: {file.as_posix()}")
        return getattr(self, f"read_{file.suffix[1:]}").__call__(file)

    @staticmethod
    def __unite(values: Iterable, joint: str = BREAK) -> str:
        unite = lambda values: joint.join(tuple(map(str, values)))
        united_arg_values = unite(values) if isinstance(values, (list, tuple)) else str(values)
        logger.debug(f"{values} > {united_arg_values}")
        return united_arg_values

    @staticmethod
    def __clean(long_string: str) -> str:
        """
        exiftool or gdal_translate commands
        have syntax of their own - hence this cleaning.
        """
        cleand_string = long_string.replace("= ", "=")
        logger.debug(cleand_string)
        return cleand_string

    def preprocess_args(self, arguments: Union[Dict, List]):

        # converting to list
        arguments = list(arguments.items()) if isinstance(arguments, dict) else arguments
        if isinstance(arguments, (list, tuple)):
            # Handling [**, ("arg_store") | ("arg_store", ), **] inputs
            arguments = [A if len(A) == 2 else tuple([*list(A), ""]) for A in arguments]
        return [(argument, self.__unite(value)) for argument, value in arguments]

    @singledispatchmethod
    def process_arg(self, args: Union[str, Path, Dict]):

        r"""Processes the arg as in a more handy manner.

            This can be called as
            .. function:: process_arg(str)
            .. function:: process_arg(dict)
            .. function:: process_arg(Path)

                        depending on the convenience.
            Returns:
                str: the command processible by subprocess.Popen

            Example::
                >>> args = {"subp.py": {"--arg_one": 102, "--arg_two": 205}}
                >>> PrettyPopen.process_arg(args, *, **)
                "python subp.py --arg_one 102 --arg_two 205"

                >>> args = "path_to_arg.json" # json:= {"subp.py": "--arg_one": 102, "--arg_two": 205}
                >>> PrettyPopen.process_arg(args, *, **)
                "python subp.py --arg_one 102 --arg_two 205"

                >>> args = "path_to_arg.yaml" # yaml:= subp.py:\n - --arg_one: 102\n - --arg_two: 205\n
                >>> PrettyPopen.process_arg(args, *, **)
                "python subp.py --arg_one 102 --arg_two 205"

                >>> args = "python subp.py --arg_one 102 --arg_two 205"
                >>> PrettyPopen.process_arg(args, *, **)
                "python subp.py --arg_one 102 --arg_two 205"
                """
        logger.debug(f"PrettyPopen arg passed as {type(args)}")
        raise NotImplementedError

    @process_arg.register
    def _(self, args: str):
        args_file = Path(args)
        if args_file.exists():
            return self.process_arg(args_file)
        return args

    @process_arg.register
    def _(self, args: Path) -> str:
        return self.process_arg(self.read_file(file=args))

    @process_arg.register
    def _(self, args: dict) -> str:
        assert self.is_proper_dict(args=args)
        try:
            # It is assumed that each cmd is about one process,
            # hence the length of the dict is 1.
            command = next(iter(args))
            arguments = args[command]
            arguments = self.preprocess_args(arguments)
            arguments = self.__unite([self.__unite(argument) for argument in arguments])
            return self.__unite([command, self.__clean(arguments)])
        except Exception as exc:
            logger.exception(exc)
            raise
