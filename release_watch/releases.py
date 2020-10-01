from datetime import datetime, timedelta

import humanize
import requests
from rich.console import Console
from rich.progress import track
from rich.table import Table
from rich.text import Text
from functools import lru_cache
from release_watch import configuration


def get_latest_release(s, sub_url):
    # Dummy date is needed for sort
    published_at = "1990-01-01T00:00:00Z"
    name = None
    tag_name = None
    r = s.get(f"https://api.github.com/repos/{sub_url}/releases/latest")
    if r.ok:
        tag_name = r.json()["tag_name"]
        published_at = r.json()["published_at"]
        name = r.json()["name"]
    else:
        r = s.get(
            f"https://api.github.com/repos/{sub_url}/tags",
        )
        if r.ok:
            tag_name = r.json()[0]["name"]
    return sub_url, published_at, tag_name, name


@lru_cache(maxsize=512)
def human_date(dt):
    if dt == "1990-01-01T00:00:00Z":
        return None
    elif dt:
        diff = datetime.now() - datetime.fromisoformat(dt[:-1])
        if diff <= timedelta(days=7):
            return Text.assemble((humanize.naturaltime(diff), "bold green"))
        elif diff <= timedelta(days=30):
            return Text.assemble((humanize.naturaltime(diff), "bold orange3"))
        else:
            return Text.assemble((humanize.naturaltime(diff), "bold red"))


def get_all_releases(s, sub_urls):
    _releases = []
    for s_url in track(sub_urls, description="Fetching releases..."):
        _releases.append(get_latest_release(s, s_url))
    return sort_releases(_releases)


def sort_releases(tuplist):
    return sorted(tuplist, key=lambda x: x[1], reverse=True)


def main():
    c = configuration.Config()
    GITHUB_USER = c.conf["github_user"]
    GITHUB_TOKEN = c.conf["github_token"]
    SUB_URLS = c.conf["sub_urls"]

    console = Console()
    s = requests.Session()
    s.auth = (GITHUB_USER, GITHUB_TOKEN)

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Project", style="bold white")
    table.add_column("Updated")
    table.add_column("Tag")
    table.add_column("Name")

    for c1, c2, c3, c4 in get_all_releases(s, SUB_URLS):
        table.add_row(c1, human_date(c2), c3, c4)

    console.print(table)
    # print(human_date.cache_info())


if __name__ == "__main__":
    main()
