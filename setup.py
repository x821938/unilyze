import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unilyze",
    version="0.1.0",
    author="Alex Skov Jensen",
    author_email="pydev@offline.dk",
    description="Get detailed unicode information about characters and text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/x821938/unilyze",
    packages=["unilyze"],
    include_package_data=True,
    license="MIT",
    keywords=["unicode", "codepoint", "text", "character", "information", "ucd", "language"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Localization",
        "Topic :: Text Processing :: Filters",
        "Topic :: Text Processing :: General",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Text Editors :: Text Processing",
        "Intended Audience :: Developers",
    ],
    project_urls={
        "Documentation": "https://github.com/x821938/unilyze",
        "Source": "https://github.com/x821938/unilyze",
    },
    install_requires=[],
)
