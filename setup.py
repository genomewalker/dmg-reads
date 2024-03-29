from setuptools import setup
import versioneer

requirements = [
    "pandas>=1.4.2",
    "tqdm>=4.64.1",
    "pysam>=0.17.0",
    "numpy>=1.21.2",
    "biopython>=1.79",
]

setup(
    setup_requires=[
        # Setuptools 18.0 properly handles Cython extensions.
        "setuptools>=39.1.0",
        "Cython>=0.29.24",
    ],
    name="dmg-reads",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="A simple tool to extract damaged reads from BAM files",
    license="MIT",
    author="Antonio Fernandez-Guerra",
    author_email="antonio@metagenomics.eu",
    url="https://github.com/genomewalker/dmg-reads",
    packages=["dmg_reads"],
    entry_points={"console_scripts": ["dReads=dmg_reads.__main__:main"]},
    install_requires=requirements,
    keywords="dmg-reads,GTDB",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
