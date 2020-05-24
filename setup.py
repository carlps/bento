from setuptools import find_packages, setup

test_deps = [
    'coverage',
    'pytest',
]
extras = {
    'test': test_deps,
}

setup(
    name='bento',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    tests_require=test_deps,
    extras_require=extras,
)
