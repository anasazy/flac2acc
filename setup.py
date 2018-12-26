from setuptools import setup

setup(
	name='flac2acc',
	version='0.1.0',
	py_modules=['flac2acc'],
	install_requires=[
		'click',
		'colorama'
	],
	entry_points='''
		[console_scripts]
		flac2acc=flac2acc:cli
	''',
)
