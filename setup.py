import distribute_setup
distribute_setup.use_setuptools()

import os

# disables creation of .DS_Store files inside tarballs on Mac OS X
os.environ['COPY_EXTENDED_ATTRIBUTES_DISABLE'] = 'true'
os.environ['COPYFILE_DISABLE'] = 'true'

def relative_path(path):
	"""
	Return the given path relative to this file.
	"""
	return os.path.join(os.path.dirname(__file__), path)

def autosetup():
	from setuptools import setup, find_packages
    
	with open(relative_path('requirements.txt'), 'rU') as f:
		requirements_txt = f.read().split("\n")

	# check if installed with git data (not via PyPi)
	with_git = os.path.isdir(relative_path('.git'))

	return setup(
		name			= "wikiquote-extractor",
		version			= "1.0",
		
		include_package_data = True,
		zip_safe		= False,
		packages		= find_packages(),
		
		entry_points	= {
			'console_scripts': [
				'wikiquote-extractor = wikiquote_extractor.app:main',
			]
		},
		
		setup_requires = ["setuptools_git >= 0.4.2"] if with_git else [],
		install_requires = requirements_txt,
	)

if(__name__ == '__main__'):
	dist = autosetup()
