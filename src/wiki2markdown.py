"""wikipedia to markdown"""

import re
from pathlib import Path

import click
from langchain_community.document_loaders import WikipediaLoader


def convert_headings(page_content: str) -> str:
    """Convert headings

    Args:
        page_content (str): wikipedia page content

    Returns:
        str: markdown page content
    """
    for level in range(6, 1, -1):
        page_content = re.sub(
            rf"{'=' * level} ([^=]+) {'=' * level}",
            rf"{'#' * level} \1",
            page_content,
        )
    return page_content


def wikipedia_to_markdown(topic: str, lang: str = "ja") -> str:
    """Wikipedia page to markdown format

    Args:
        topic (str): wikipedia topic
        lang (str, optional): \
            language code for the Wikipedia language edition. Defaults to "ja".

    Returns:
        str: markdown text
    """
    doc = WikipediaLoader(
        topic,
        lang=lang,
        load_max_docs=1,
        doc_content_chars_max=300000,
    ).load()[0]

    markdown_text = f"# {topic}\n\n"
    page_content = convert_headings(doc.page_content)
    sections = re.split(r"\n(## .*)\n", page_content)
    for i in range(0, len(sections), 2):
        if i + 1 < len(sections) and any(
            line.strip() for line in sections[i + 1].split("\n")
        ):
            markdown_text += f"{sections[i]}\n{sections[i+1]}\n\n"

    return markdown_text


@click.command()
@click.option(
    "--topic",
    type=str,
    required=True,
    help="wikipedia topic",
)
@click.option(
    "--output_dir",
    type=Path,
    required=True,
    help="markdown output dirpath",
)
@click.option(
    "--lang",
    type=str,
    required=False,
    default="ja",
    help="language code for the Wikipedia language edition",
)
def main(topic: str, output_dir: Path, lang: str = "ja") -> None:
    """main

    Args:
        topic (str): wikipedia topic
        output_dir (Path): markdown output dirpath
        lang (str, optional): \
            language code for the Wikipedia language edition. Defaults to "ja".
    """
    markdown_text = wikipedia_to_markdown(topic=topic, lang=lang)

    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir.joinpath(f"{topic.replace(' ', '_')}.md")
    filepath.write_text(markdown_text)

    print(f"Markdown file created: {filepath.as_posix()}")


if __name__ == "__main__":
    main()
