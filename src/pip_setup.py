import click
from pathlib import Path
from . import logging_setup 
import logging

logger = logging_setup.setup_common_logger("pip-setup")
logger.setLevel(logging.INFO)

def load_setup_file(dry:bool, name:str, root:Path)->None :
    working_file = root/name/"setup.py"
    if not working_file.exists() and not dry:
        logger.getChild('load-setup.py').error(f"file doesn't exist. exiting")
        raise Exception(f"{working_file} does not exist, cant load")
    text_to_load = f'''
from setuptools import setup, find_packages
setup(
   name='{name}',
   version='0.1.0',
   packages=find_packages(),
   install_requires=[
        # Add your dependencies here
   ],
   entry_points={{
       'console_scripts': [
           '{name}=src.{name}:main',
           ],
   }},
)
    '''
    if not dry:
        try:
            working_file.write_text(text_to_load)
        except PermissionError:
            logger.getChild('load-setup.py').error("Could not write the contents of the file due to a PermissionError")
            return False
        except OSError as e:
            logger.getChild('load-setup.py').error(f"Could not write the contents of the file due to {e}")
            return False
    logger.getChild('load-setup.py').debug(f"Wrote to file:{working_file}")
    return True


def load_main_file(dry:bool, name:str, root:Path)->None :
    working_file = root/name/'src'/f"{name}.py"
    if not working_file.exists() and not dry:
        logger.getChild('load-main.py').error(f"file doesn't exist. exiting")
        raise Exception(f"{working_file} does not exist, cant load")
    text_to_load = '''# Autocreated file
import click

@click.command()
def main():
    """A sample CLI program"""
    print(f"Hello from {__file__}")

if __name__ == "__main__":
    main()
    '''
    if not dry:
        try:
            working_file.write_text(text_to_load)
        except PermissionError:
            logger.getChild('load-main.py').error("Could not write the contents of the file due to a PermissionError")
            return False
        except OSError as e:
            logger.getChild('load-main.py').error(f"Could not write the contents of the file due to {e}")
            return False
    logger.getChild('load-main.py').debug(f"Wrote to file:{working_file}")
    return True


def touch_all_files(dry:bool, name:str, root:Path) -> bool:
    files_to_touch = [
        root / name / "src/",
        root / name / "src/__init__.py",
        root / name / f"src/{name}.py",
        root / name / "readme.md",
        root / name / "requirements.txt",
        root / name / "setup.py",
        root / name / "tests/",
    ]

    if not dry:
        (root/name).mkdir(exist_ok=True)

    for file in files_to_touch:
        if dry:
            logger.getChild('touch').debug(f"{file.absolute()} exists {'✅' if file.exists() else '❌'} file?{'📁' if file.suffix=='' else '❌'} {file.suffix=}")
        else: 
            if file.suffix == '':
                file.mkdir(parents=True, exist_ok=True)
            else:
                file.absolute().touch(exist_ok=True)
            
            logger.getChild('touch').debug(f"{file.absolute()} exists {'✅' if file.exists() else '❌'}")

@click.command()
@click.argument('name', type=str, nargs=1)
@click.option('--root', type=Path, default=".", help='The root directory where you want the files to be setup')
@click.option('--dry', is_flag=True, help='dont actually change any files')
@click.option('--verbose','-v', is_flag=True, help='verbose output')
def main(name:str, root:Path, dry:bool, verbose:bool) -> None:
    """Simple CLI Example"""
    
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("set the logging to debug mode")
    logger.info(f"verbose is {verbose}")
    if type(root) == str:
        logger.debug(f'Setting the root path to a proper POSIX path instead of a string')
        root = Path(root)
    root = root.resolve()

    logger.info(f"Hello from {__file__} with the name of {name} and a path of {root=}")
    touch_all_files(dry, name, root)
    load_setup_file(dry, name, root)
    load_main_file(dry, name, root)

if __name__ == "__main__":
    main()

