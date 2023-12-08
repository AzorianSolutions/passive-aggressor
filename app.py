import click
import os
import platform
import random
import re
import shutil
import string
from loguru import logger
from pathlib import Path

CONTEXT_SETTINGS = dict(auto_envvar_prefix="PA")

IS_DARWIN: bool = platform.system() == 'Darwin'
"""bool: Whether the current operating system is macOS."""

IS_LINUX: bool = platform.system() == 'Linux'
"""bool: Whether the current operating system is Linux."""

IS_WINDOWS: bool = platform.system() == 'Windows'
"""bool: Whether the current operating system is Windows."""

MAX_LENGTH_DARWIN: int = 1024
"""int: The maximum length of a file path on macOS."""

MAX_LENGTH_LINUX: int = 4096
"""int: The maximum length of a file path on Linux."""

MAX_LENGTH_WINDOWS: int = 260
"""int: The maximum length of a file path on Windows."""

MAX_LENGTH: int = MAX_LENGTH_DARWIN if IS_DARWIN else MAX_LENGTH_LINUX if IS_LINUX else MAX_LENGTH_WINDOWS
"""int: The maximum length of a file path on the current operating system."""

TMP_PATH: str = '/tmp' if IS_DARWIN or IS_LINUX else 'C:\\Windows\\Temp'
"""str: The path to the temporary directory on the current operating system."""

version: str = '0.1.0'
"""str: The version of the application."""


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('output', type=click.Path(), default='archive.tar.gz', nargs=1, required=True)
@click.argument('source', type=click.Path(exists=True), nargs=-1, required=True)
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode.', default=False)
@click.option('-m', '--message', type=str or None, default=None,
              help='Hidden message to be embedded in the archive file path.')
@click.version_option(version, '-V', '--version', message='%(version)s')
def cli(output: click.Path, source: tuple[str, ...], debug: bool, message: str or None):
    """A tool to create annoyingly deep file archives with an optional hidden message in the file system path."""

    env_max_length: int = MAX_LENGTH - len(TMP_PATH) - 20
    message_max: int = env_max_length - 2

    if message is not None:
        exp = re.compile(r'[\W_]+')
        message = exp.sub('', message)

    if message is not None and len(message) > message_max:
        logger.error(f'Message is too long. Maximum length is {message_max} characters.')
        return

    source_str: str = ', '.join(source)
    intro: str = f'Creating archive {output} from {source_str}'

    if message is not None:
        intro += f' with message "{message}"'

    logger.info(intro)

    compressed_path: str = ''

    while len(compressed_path) < env_max_length:
        random_chars: list = random.choices(string.ascii_letters + string.digits, k=1)
        next_char: str = random_chars[0]
        compressed_path += next_char + os.sep

    # Replace a section in the middle of the compressed path with the message broken into single character segments
    if message is not None:
        message = os.sep.join(list(message))
        message_len: int = len(message)
        message_start: int = (env_max_length - message_len) // 2
        message_end: int = message_start + message_len
        compressed_path = (compressed_path[:message_start] + os.sep + message + os.sep
                           + compressed_path[message_end:])

    tmp_path: str = TMP_PATH + os.sep + compressed_path

    if len(tmp_path) > MAX_LENGTH:
        logger.error(f'Archive path is too long. Maximum length is {MAX_LENGTH} characters.')
        return

    if debug:
        logger.debug(f'Archive Path: {compressed_path}')
        logger.debug(f'OS Platform: {platform.system()}')
        logger.debug(f'OS Max length: {MAX_LENGTH}')
        logger.debug(f'Final Max Length: {env_max_length}')
        logger.debug(f'Message Max Length: {message_max}')
        logger.debug(f'Path Length: {len(tmp_path)}')
        logger.debug(f'Creating temporary path under {TMP_PATH}')

    current_path: str = TMP_PATH + os.sep

    for directory in compressed_path.split(os.sep):
        if directory == '':
            continue

        current_path += directory + os.sep

        if not os.path.exists(current_path):
            os.mkdir(current_path)

    # Copy the source files into the temporary directory
    for source_path in source:
        source_path = Path(source_path)
        target_path: str = tmp_path + source_path.name
        if debug:
            logger.debug(f'Copying {source_path} to {target_path}')
        os.system(f'cp -r {source_path} {target_path}')

    # Create the archive based on the given output path file extension
    if str(output).endswith('.tar.gz'):
        os.system(f'tar -zcvf {output} -C {TMP_PATH} {compressed_path} >/dev/null 2>&1')
    elif str(output).endswith('.zip'):
        os.system(f'cd {TMP_PATH} && zip -r {os.path.abspath(str(output))} {compressed_path}>/dev/null 2>&1')
    else:
        logger.error(f'Unsupported archive type. Must be .tar.gz or .zip')
        return

    # Remove the temporary directory
    compressed_parts: list[str] = compressed_path.split(os.sep)[:-1]
    tmp_root: str = TMP_PATH + os.sep + compressed_parts[0]
    current_paths: list[str] = compressed_parts.copy()

    while os.path.exists(tmp_root):
        if not len(current_paths):
            break

        remove_path: str = TMP_PATH + os.sep + os.sep.join(current_paths)

        if os.path.exists(remove_path):
            shutil.rmtree(remove_path)

        current_paths.pop()

    if debug:
        logger.debug(f'Removed temporary path {tmp_root}')

    logger.success(f'Archive has been created at {output}')
