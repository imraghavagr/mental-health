import requests
import click

@click.command()
@click.argument('url')
@click.argument('path', type=click.Path())
def download_file(url, path):
    """Downloads a file from a URL to a local path."""
    print('Downloading {} to {}...'.format(url, path))
    response = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        f.write(response.content)

if __name__ == '__main__':
    download_file()