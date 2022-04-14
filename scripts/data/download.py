import requests
import click


@click.command()
@click.argument('url')
@click.argument('filename', type=click.Path())
def download_file(url, filename):
    """Downloads a file from a URL to a local file."""
    print('Downloading {} to {}...'.format(url, filename))
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        f.write(response.content)

if __name__ == '__main__':
    download_file()