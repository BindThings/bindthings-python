from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name             = "bindthings",
    version          = "1.0.0",
    author           = "BindThings",
    author_email     = "getbindthings@gmail.com",
    description      = "Official Python client for BindThings IoT Platform",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url              = "https://github.com/bindthings/bindthings-python",
    packages         = find_packages(),
    python_requires  = ">=3.7",
    install_requires = ["paho-mqtt>=1.6.0"],
    classifiers      = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Home Automation",
    ],
    keywords = "iot mqtt bindthings telemetry raspberry-pi",
)
