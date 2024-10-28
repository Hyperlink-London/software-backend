import subprocess
import typer
from ._utils import set_dev_mode
from .constants import (APPLICATION_NAME, APPLICATION_PORT, APPLICATION_HOST,
                        APPLICATION_PORT_DEV, APPLICATION_HOST_DEV)
from .logger import logger

cli = typer.Typer(add_completion=False)


@cli.command(name=APPLICATION_NAME)
def launch_api_server(
        host: str = APPLICATION_HOST_DEV,
        port: str = APPLICATION_PORT_DEV,
        dev: bool = False
):
    """Launch the hyperlink API server."""
    set_dev_mode(dev)
    command = ['uvicorn', 'hyperlink_api:app']

    # Set default values if in dev mode
    if dev:  # TODO: add support for other dev environments
        command.append('--reload')
    else:
        command.append('--workers')
        command.append('1')

    port = APPLICATION_PORT
    host = APPLICATION_HOST
    # Update the command with host and port information
    command.extend(['--port', str(port)])
    command.extend(['--host', host])

    logger.warning(f"Launching API server at {host}:{port}")
    subprocess.run(command)
