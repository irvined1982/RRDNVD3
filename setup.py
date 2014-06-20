import os
from setuptools import setup


setup(
		name='django-openlavaweb',
		version='1.0',
		packages=['rrdviewer'],
		include_package_data=True,	
		license="GPL v2",
		description="RRDViewer is a django application that produces NVD3 graphs of RRD databasees.",
		#url="http://www.clusterfsck.io/rrdviewer",
		author="David Irvine",
		author_email="irvined@gmail.com",
		classifiers=[
			'Environment :: Web Environment',
			'Framework :: Django',
			'Programming Language :: Python',
			'Operating System :: OS Independent',
			'Programming Language :: Python :: 2',
			'Programming Language :: Python :: 2.7',
			'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
			'Intended Audience :: System Administrators',
			],
		)
