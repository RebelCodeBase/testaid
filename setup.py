import os
import setuptools

if __name__ == '__main__':
    setuptools.setup(
        name='testaid',
        version='0.1',
        author='RebelCodeBase',
        author_email='rebelcodebase@riseup.net',
        description='Fixtures for testinfra and molecule',
        long_description=open(os.path.join(
            os.path.dirname(__file__), 'README.rst')).read(),
        url='https://github.com/RebelCodeBase/testaid',
        license='Apache-2.0',
        packages=setuptools.find_packages(),
        install_requires=['docutils>=0.3', 'testinfra>=3.0.5', 'molecule>=2.20.2'],
        setup_requires=['pytest-runner'],
        tests_require=['pytest'],
        package_data={
            '': ['*.rst'],
        },
        zip_safe=False,
    )
