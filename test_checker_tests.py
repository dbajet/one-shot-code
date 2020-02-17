import io
import os
from pathlib import Path
from typing import List, Optional

from scripts.checker_tests import CheckerTests

root_path = Path(__file__).parent.parent.parent.absolute().as_posix()  # /app


def test___init__():
    tested = CheckerTests()

    result = tested.untested_functions
    expected: List = []
    assert expected == result

    result = tested.output
    assert result is None


def test_flat_class_name():
    tested = CheckerTests
    tests = [
        ('Class', 'class'),
        ('MyClass', 'my_class'),
        ('MyABClass', 'my_abclass'),
        ('', ''),
    ]
    for value, expected in tests:
        result = tested.flat_class_name(value)
        assert expected == result


def test_testable_functions():
    tested = helper_instance()
    tests = [
        ('scripts/tests/checker_tests/level1/for_checker_level1.py', [
            'function_checker_level1a',
            'function_checker_level1b',
            'function_checker_level1c',
        ]),
        ('scripts/tests/checker_tests/level1/for_checker_mix_class_procedure.py',
         ['function', 'procedure']),
        ('scripts/tests/checker_tests/level1/for_checker_multi_classes.py', [
            '_function_1',
            'for_checker_a___init__',
            'for_checker_a_function_1',
            'for_checker_b___init__',
            'for_checker_b_function_1',
            'function_2',
            'function_3',
        ]),
    ]
    for file, expected in tests:
        result = tested.testable_functions(f'{root_path}/{file}')
        assert expected == result


def test_test_directory_of():
    tested = helper_instance()
    tests = [
        (f'{root_path}/scripts/tests/checker_tests/level1/for_checker_level1.py',
         f'{root_path}/scripts/tests/checker_tests/testings/level1/tilt_for_checker_level1.py'),
        (f'{root_path}/scripts/unknown.py', None),
        (f'{root_path}/unknown/unknown.py', None),
    ]
    for file, expected in tests:
        result = tested.test_directory_of(file)
        assert expected == result


def test_tested_functions():
    tested = helper_instance()

    tests = [
        # simple file
        (f'{root_path}/scripts/tests/checker_tests/level1/for_checker_level1.py', [
            'function_checker_level1b',
            'function_checker_level1c',
        ]),
        # file functions with identical name + multiple test functions for the same method
        (f'{root_path}/scripts/tests/checker_tests/level1/for_checker_fully_tested.py', [
            '_function_checker_fully_tested_c',
            'fully_tested_function_checker_fully_tested_c',
            'function_checker_fully_tested_a',
            'function_checker_fully_tested_b',
        ]),
        # file with test in class
        (f'{root_path}/scripts/tests/checker_tests/level1/for_checker_test_class.py', [
            '__init__',
            'function_with_test',
        ]),
    ]
    for file, expected in tests:
        result = tested.tested_functions(file)
        assert expected == result


def test_add_untested_functions():
    tested = helper_instance()

    spaces = ' ' * 51

    # initialized to empty list
    result = tested.untested_functions
    expected: List = []
    assert expected == result

    # adding one untested method
    tested.add_untested_functions('filepath1', 'method1')
    expected = [
        f'filepath1{spaces}: method1 is not tested.',
    ]
    assert expected == result

    # adding more untested methods
    tested.add_untested_functions('filepath2', 'method1')
    tested.add_untested_functions('filepath1', 'method2')
    tested.add_untested_functions('filepath1', 'method1')
    expected = [
        f'filepath1{spaces}: method1 is not tested.',
        f'filepath2{spaces}: method1 is not tested.',
        f'filepath1{spaces}: method2 is not tested.',
        f'filepath1{spaces}: method1 is not tested.',
    ]
    assert expected == result


def test_testable_files():
    tested = helper_instance()
    result = tested.testable_files(f'{root_path}/scripts/tests/checker_tests/')
    expected = [
        f'{root_path}/scripts/tests/checker_tests/level1/for_checker_fully_tested.py',
        f'{root_path}/scripts/tests/checker_tests/level1/for_checker_level1.py',
        f'{root_path}/scripts/tests/checker_tests/level1/for_checker_mix_class_procedure.py',
        f'{root_path}/scripts/tests/checker_tests/level1/for_checker_multi_classes.py',
        f'{root_path}/scripts/tests/checker_tests/level1/for_checker_test_class.py',
        f'{root_path}/scripts/tests/checker_tests/level1/level2/for_checker_level2.py',
        f'{root_path}/scripts/tests/checker_tests/level1/level2/level3/for_checker_level3.py',
    ]
    assert expected == result


def test_write(capsys):
    # print in sys out
    tested = CheckerTests()
    tested.write('This is a test')
    result = capsys.readouterr()
    expected = 'This is a test\n'
    assert expected == result.out
    expected = ''
    assert expected == result.err

    # print in buffer
    output = io.StringIO()
    tested = CheckerTests(output)
    tested.write('This is a test')
    result_out = output.getvalue()
    expected = 'This is a test\n'
    assert expected == result_out

    result = capsys.readouterr()
    expected = ''
    assert expected == result.out
    expected = ''
    assert expected == result.err


def test_full_path_of(monkeypatch):

    def get_root():
        return root_path

    monkeypatch.setattr(os, 'getcwd', get_root)
    output = io.StringIO()
    tested = helper_instance(output)
    tests = [
        # directories
        ('/some/path', '/some/path'),
        ('some/path', f'{root_path}/some/path'),
        # file
        ('/some/path/file.py', '/some/path/file.py'),
        ('some/path/file.py', f'{root_path}/some/path/file.py'),
        # test files are translated to the source file
        ('/some/testings/path', '/some/path'),
        ('some/testings/path', f'{root_path}/some/path'),
        ('/some/testings/path/tilt_file.py', '/some/path/file.py'),
        ('some/testings/path/tilt_file.py', f'{root_path}/some/path/file.py'),
    ]
    for a_path, expected in tests:
        result = tested.full_path_of(a_path)
        assert expected == result


def test_run__single_file():
    output = io.StringIO()
    tested = helper_instance(output)
    tested.run([f'{root_path}/scripts/tests/checker_tests/level1/for_checker_level1.py'])
    result = tested.output.getvalue()
    expected = [
        '--- UNTESTED ---',
        f'{root_path}/scripts/tests/checker_tests/level1/for_checker_level1.py: function_checker_level1a is not tested.',
        '--- -------- ---',
        '',
    ]
    assert '\n'.join(expected) == result


def test_run__single_directory():
    output = io.StringIO()
    tested = helper_instance(output)
    tested.run([f'{root_path}/scripts/tests/checker_tests/level1/level2'])
    result = tested.output.getvalue()
    expected = [
        '--- UNTESTED ---',
        f'{root_path}/scripts/tests/checker_tests/level1/level2/for_checker_level2.py: function_checker_level2b is not tested.',
        f'{root_path}/scripts/tests/checker_tests/level1/level2/level3/for_checker_level3.py: whole file is not tested.',
        '--- -------- ---',
        '',
    ]
    assert '\n'.join(expected) == result


def test_run__multiple_entry():
    output = io.StringIO()
    tested = helper_instance(output)
    tested.run([
        f'{root_path}/scripts/tests/checker_tests/level1/level2',
        f'{root_path}/scripts/tests/checker_tests/level1/for_checker_fully_tested.py',
        f'{root_path}/scripts/tests/checker_tests/level1/for_checker_mix_class_procedure.py',
        f'{root_path}/scripts/tests/checker_tests/level1/for_checker_multi_classes.py',
        f'{root_path}/scripts/tests/checker_tests/level1/for_checker_test_class.py',
    ])
    result = tested.output.getvalue()
    expected = [
        '--- UNTESTED ---',
        f'{root_path}/scripts/tests/checker_tests/level1/level2/for_checker_level2.py: function_checker_level2b is not tested.',
        f'{root_path}/scripts/tests/checker_tests/level1/level2/level3/for_checker_level3.py: whole file is not tested.',
        f'{root_path}/scripts/tests/checker_tests/level1/for_checker_mix_class_procedure.py: function is not tested.',
        f'{root_path}/scripts/tests/checker_tests/level1/for_checker_multi_classes.py: for_checker_a___init__ is not tested.',
        f'{root_path}/scripts/tests/checker_tests/level1/for_checker_multi_classes.py: for_checker_b_function_1 is not tested.',
        f'{root_path}/scripts/tests/checker_tests/level1/for_checker_multi_classes.py: function_3 is not tested.',
        f'{root_path}/scripts/tests/checker_tests/level1/for_checker_test_class.py: function_without_test is not tested.',
        '--- -------- ---',
        '',
    ]
    assert '\n'.join(expected) == result


def test_run__test_files():
    output = io.StringIO()
    tested = helper_instance(output)
    tested.run([
        f'{root_path}/scripts/tests/checker_tests/testings/level1/tilt_for_checker_fully_tested.py',
        f'{root_path}/scripts/tests/checker_tests/testings/level1/level2/tilt_for_checker_level2.py',
    ])
    result = tested.output.getvalue()
    expected = [
        '--- UNTESTED ---',
        f'{root_path}/scripts/tests/checker_tests/level1/level2/for_checker_level2.py: function_checker_level2b is not tested.',
        '--- -------- ---',
        '',
    ]
    assert '\n'.join(expected) == result


def test_run__nothing_to_test():
    output = io.StringIO()
    tested = helper_instance(output)
    tested.run([])
    result = tested.output.getvalue()
    expected = [
        'Nothing to check',
        '',
    ]
    assert '\n'.join(expected) == result


def test_run__auto_check():
    output = io.StringIO()
    tested = CheckerTests(output)
    tested.run([f'{root_path}/scripts/checker_tests.py'])
    result = tested.output.getvalue()
    expected = [
        'All methods are tested!',
        '',
    ]
    assert '\n'.join(expected) == result


def helper_instance(output: Optional[io.StringIO] = None):
    tested = CheckerTests(output)
    tested.TEST_DIRECTORY = 'testings'
    tested.TEST_PREFIX_FILE = 'tilt_'
    tested.TEST_PREFIX_FUNCTION = 'testing_'
    return tested
