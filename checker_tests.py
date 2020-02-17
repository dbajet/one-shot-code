#!/usr/bin/env python3

import ast
import io
import os
import re
import sys
from os import path, listdir
from typing import List, Dict, Optional


class CheckerTests:
    TEST_DIRECTORY = 'tests'
    TEST_PREFIX_FILE = 'test_'
    TEST_PREFIX_FUNCTION = 'test_'

    def __init__(self, output: Optional[io.StringIO] = None):
        self.untested_functions: List = []
        self.output = output

    @staticmethod
    def flat_class_name(camel_cases: str) -> str:
        return re.sub('(?!^)([A-Z]+)', r'_\1', camel_cases).lower()

    def testable_functions(self, filepath: str) -> List[str]:
        result: List = []
        function_grouped: Dict = {}
        # retrieve all procedures and class methods
        with open(filepath, 'rt') as file:
            tree = ast.parse(file.read(), filename=filepath)
            for item in tree.body:
                if isinstance(item, ast.FunctionDef):
                    if item.name not in function_grouped:
                        function_grouped[item.name] = []
                    function_grouped[item.name].append('')
                elif isinstance(item, ast.ClassDef):
                    for node in ast.iter_child_nodes(item):
                        if isinstance(node, ast.FunctionDef):
                            if node.name not in function_grouped:
                                function_grouped[node.name] = []
                            function_grouped[node.name].append(item.name)

        # add a prefix to any function that is defined in more than one place
        for method, classes in function_grouped.items():
            for class_name in classes:
                prefix = ''
                if len(classes) > 1:
                    prefix = f'{self.flat_class_name(class_name)}_'
                result.append(f'{prefix}{method}')
        return sorted(result)

    def test_directory_of(self, filepath: str) -> Optional[str]:
        if not path.isfile(filepath):
            return None
        basename = path.basename(filepath)
        for slash in re.finditer('/', filepath):
            index = slash.start()
            directory = f'{filepath[:index]}/{self.TEST_DIRECTORY}'
            if path.exists(directory) and path.isdir(directory):
                return ''.join([
                    directory,
                    filepath[index:-1 * len(basename)],
                    self.TEST_PREFIX_FILE,
                    basename,
                ])
        return None

    def tested_functions(self, filepath: str) -> List[str]:
        result: List = []
        # retrieve the test directory and build the test filename
        test_filepath = self.test_directory_of(filepath)
        if not (test_filepath and path.exists(test_filepath)):
            return result
        # retrieve all tested functions
        function_patterns = [
            # for magic methods: test_class___init__
            re.compile(f'^{self.TEST_PREFIX_FUNCTION}(.+__.+__)$'),
            # for methods with several tests: test_method__partial
            re.compile(f'^{self.TEST_PREFIX_FUNCTION}(.+)__.+$'),
            # for regular methods: test_method
            re.compile(f'^{self.TEST_PREFIX_FUNCTION}(.+)$'),
        ]
        with open(test_filepath, 'rt') as file:
            tree = ast.parse(file.read(), filename=test_filepath)
            for item in tree.body:
                if isinstance(item, ast.FunctionDef):
                    for pattern in function_patterns:
                        match = pattern.search(item.name)
                        if match:
                            result.append(match[1])
                            break
                elif isinstance(item, ast.ClassDef):
                    for node in ast.iter_child_nodes(item):
                        if isinstance(node, ast.FunctionDef):
                            for pattern in function_patterns:
                                match = pattern.search(node.name)
                                if match:
                                    result.append(match[1])
                                    break

        return sorted(list(set(result)))

    def add_untested_functions(self, filepath: str, function: str):
        self.untested_functions.append(f'{filepath:<60}: {function} is not tested.')

    def testable_files(self, directory: str) -> List[str]:
        result: List = []
        if directory[-1:] == '/':
            directory = directory[:-1]
        for item in listdir(directory):
            full_path = f'{directory}/{item}'
            if path.isdir(full_path):
                if item[0] == '.':
                    continue
                if item not in [self.TEST_DIRECTORY, '__pycache__']:
                    result.extend(self.testable_files(full_path))
            if path.isfile(full_path) and item[-3:] == '.py':
                result.append(full_path)
        return sorted(result)

    def write(self, message: str):
        if self.output:
            self.output.write(f'{message}\n')
        else:
            print(message)

    def full_path_of(self, a_path: str) -> str:
        # test files are changed to the source files
        patterns = [
            r'^(.*/){directory}/(.*){prefix}([^/]+\.py)$'.format(
                directory=self.TEST_DIRECTORY, prefix=self.TEST_PREFIX_FILE),
            r'^(.*/){directory}/(.*)$'.format(directory=self.TEST_DIRECTORY),
        ]
        for pattern in patterns:
            match = re.search(pattern, a_path)
            if match:
                a_path = ''.join(match.groups())
                break
        # absolute paths are kept
        if a_path[0] == '/':
            return a_path
        return os.path.realpath(f'{os.getcwd()}/{a_path}')

    def run(self, paths: List[str]):
        files: List = []
        # build the list of files to parse
        for full_path in map(self.full_path_of, paths):
            if os.path.basename(full_path).startswith(self.TEST_PREFIX_FILE):
                continue
            if path.isfile(full_path):
                files.append(full_path)
            elif path.isdir(full_path):
                if full_path[-1:] == '/':
                    full_path = full_path[:-1]
                for filepath in self.testable_files(full_path):
                    files.append(filepath)
        # parse each file
        for filepath in files:
            functions = self.testable_functions(filepath)
            tested = self.tested_functions(filepath)
            if tested:
                for function in functions:
                    if function not in tested:
                        self.add_untested_functions(filepath, function)
            elif functions:
                self.add_untested_functions(filepath, 'whole file')
        # display the results
        if self.untested_functions:
            self.write('--- UNTESTED ---')
            for method in self.untested_functions:
                self.write(method)
            self.write('--- -------- ---')
        elif files:
            self.write('All methods are tested!')
        else:
            self.write('Nothing to check')


if __name__ == '__main__':
    helper = CheckerTests()
    if len(sys.argv) > 1:
        helper.run(sys.argv[1:])
    else:
        print('provide at least one path')
    exit(0)
