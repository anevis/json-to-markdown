import io
import json
from typing import Dict, Any, Optional

import click
import yaml

from yaml_to_markdown.md_converter import MDConverter


def _get_json_data(json_file: str) -> Dict[str, Any]:
    with io.open(json_file, "r", encoding="utf-8") as j_file:
        return json.load(j_file)


def _get_yaml_data(yaml_file: str) -> Dict[str, Any]:
    with io.open(yaml_file, "r", encoding="utf-8") as y_file:
        return yaml.safe_load(y_file)


def _help() -> None:
    click.echo("Convert JSON or YAML to Markdown.")
    click.echo(
        "Usage: yaml-to-markdown -o <output_file> [-y <yaml_file> | -j <json_file>]"
    )
    click.echo(
        "    -o, --output-file <output_file>: Path to the output file as a string [Mandatory]."
    )
    click.echo(
        "    -y, --yaml-file <yaml_file>: Path to the YAML file as a string [Optional]"
    )
    click.echo(
        "    -j, --json-file <json_file>: Path to the JSON file as a string [Optional]"
    )
    click.echo("    -h, --help: Show this message and exit.")
    click.echo(
        "Note: Either yaml_file or json_file is required along with output_file."
    )
    click.echo("Example: yaml-to-markdown -o output.md -y data.yaml")


@click.command()
@click.option("-o", "--output-file", "output_file", type=str)
@click.option("-y", "--yaml-file", "yaml_file", type=str, default=None)
@click.option("-j", "--json-file", "json_file", type=str, default=None)
@click.option("-h", "--help", "show_help", default=False, is_flag=True)
def main(
    output_file: str,
    yaml_file: Optional[str],
    json_file: Optional[str],
    show_help: bool,
) -> None:
    if show_help:
        _help()
        return
    _verify_inputs(output_file=output_file, yaml_file=yaml_file, json_file=json_file)

    convert(output_file=output_file, yaml_file=yaml_file, json_file=json_file)


def _verify_inputs(
    output_file: str, yaml_file: Optional[str], json_file: Optional[str]
) -> None:
    if (yaml_file is None and json_file is None) or output_file is None:
        _help()
        exit(1)


def convert(
    output_file: str, yaml_file: Optional[str] = None, json_file: Optional[str] = None
) -> None:
    _verify_inputs(output_file=output_file, yaml_file=yaml_file, json_file=json_file)

    data = _get_json_data(json_file) if json_file else _get_yaml_data(yaml_file)
    with io.open(output_file, "w", encoding="utf-8") as md_file:
        MDConverter().convert(data=data, output_writer=md_file)


if __name__ == "__main__":
    main()
