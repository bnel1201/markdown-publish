import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="convert-notes-bjnelson", # Replace with your own username
    version="0.0.1",
    author="Example Author",
    author_email="bnel1201@gmail.com",
    description="A small package for publishing linked markdown documents to linked htmls",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bnel1201/markdown-publish",
    project_urls={
        "Bug Tracker": "https://github.com/bnel1201/markdown-publish/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'src'},
    data_files=[('Lib/site-packages/convert_notes', ['src/convert_notes/pandoc.css'])],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    requires=[
              'fire',
              'pandoc_eqnos',
              'pandoc_fignos'
              'pandoc_tablenos',
              'pandoc_secnos'
    ]
)
