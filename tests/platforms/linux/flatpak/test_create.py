import pytest

from briefcase.console import Console, Log
from briefcase.exceptions import UnsupportedHostError
from briefcase.platforms.linux.flatpak import LinuxFlatpakCreateCommand


@pytest.fixture
def create_command(tmp_path):
    return LinuxFlatpakCreateCommand(
        logger=Log(),
        console=Console(),
        base_path=tmp_path / "base_path",
        data_path=tmp_path / "briefcase",
    )


@pytest.mark.parametrize("host_os", ["Darwin", "Windows", "WeirdOS"])
def test_unsupported_host_os(create_command, host_os):
    """Error raised for an unsupported OS."""
    create_command.tools.host_os = host_os

    with pytest.raises(
        UnsupportedHostError,
        match="Flatpaks can only be built on Linux.",
    ):
        create_command()


def test_output_format_template_context(create_command, first_app_config, tmp_path):
    """The template context is provided flatpak details."""
    first_app_config.flatpak_runtime = "org.beeware.Platform"
    first_app_config.flatpak_runtime_version = "37.42"
    first_app_config.flatpak_sdk = "org.beeware.SDK"

    assert create_command.output_format_template_context(first_app_config) == {
        "flatpak_runtime": "org.beeware.Platform",
        "flatpak_runtime_version": "37.42",
        "flatpak_sdk": "org.beeware.SDK",
    }
