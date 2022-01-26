import setuptools

setuptools.setup(
    name="xmlego",
    version="0.1",
    author="Gallay David",
    author_email="davidtennis96@hotmail.com",
    description="A module to bundle xml using xpath",
    setup_requires=['setuptools-markdown'],
    long_description_content_type="text/markdown",
    long_description_markdown_filename='README.md',
    url="https://github.com/divad1196/XMLego",
    packages=setuptools.find_packages(),
    install_requires=[
        "igraph",
        "lxml",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)