"""SwimAth - Swimming Style Analysis Application
Windows-first desktop application for analyzing swimming technique using ML
"""

from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="swimath",
    version="0.1.0",
    author="Vitek",
    description="Swimming style analysis using computer vision and machine learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vitek/swimath",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
    ],
    python_requires=">=3.11,<4.0",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "swimath=src.main:main",
        ],
    },
)
