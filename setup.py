from setuptools import setup, find_packages

setup(
    name='django-secure-contact-form',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=4.0',
        'django-simple-captcha>=0.5.14',
        'Pillow>=8.0.0',
    ],
    license='MIT',
    description='A secure and customizable contact form for Django projects.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Gavin-Humphrey/django-secure-contact-form',
    author='Gavin Humphrey',
    author_email='gavin.humphrey.pro@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)