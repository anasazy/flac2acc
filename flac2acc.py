from pathlib import Path
import subprocess

import click

# ================================================= #

def _get_cwd() -> Path:
	"""Return the current working directory as Path object"""

	return str(Path.cwd())

def _convert_to_alac(flac_file: Path, out: str) -> None:
	"""???"""

	aiff = Path(out) / (flac_file.stem + '.aiff')
	alac = Path(out) / (flac_file.stem + '.m4a')

	# Step 1: flac 2 aiff
	command = [
		'flac',
		'-s', # silent
		'-f', # force / overwrite existing files
		'-d', # decode
		'--force-aiff-format',
		'-o', aiff, # output file
		flac_file # input file
	]
	subprocess.call(command)

	# Step 2: aiff 2 m4a
	command = [
		'afconvert',
		'-f', 'm4af', # output format
		'-d', 'alac', # input format
		aiff, # input file
		alac # output file
	]
	subprocess.call(command)

	# Step 3: Clean up
	aiff.unlink()

# =========================================================================== #

@click.command()
@click.option('-d', '--debug',
	is_flag=True,
	default=False,
	help='Show additional information'
)
@click.option('-f', '--force',
	is_flag=True,
	default=False,
	help='Overwrite existing files'
)
@click.option('-o', '--out',
	type=click.Path(exists=True, file_okay=False, writable=True, resolve_path=True),
	help='Output dir'
)
@click.argument('src',
	type=click.Path(exists=True, file_okay=False, writable=True, resolve_path=True),
	default=_get_cwd,
	metavar='<source dir>'
)
def cli(debug, force, out, src):
	"""Convert *.flac files into *.m4a files"""

	if debug:
		click.echo(f'Source dir is {src}')

	# If no output dir was set, use the src dir instead
	if not out:
		out = str(src)

	src_dir = Path(src)
	flac_files = []

	for flac_file in src_dir.glob('*.flac'):
		flac_files.append(flac_file)

	count = len(flac_files)

	if count > 0:
		click.echo(f'Number of files to convert: {count}')
		with click.progressbar(flac_files, label='Converting files') as bar:
			for flac_file in bar:
				_convert_to_alac(flac_file, out)
	else:
		click.echo('No *.flac files found')
	
	click.echo('Done 🎉')

# if __name__ == '__main__':
# 	flac2acc()
