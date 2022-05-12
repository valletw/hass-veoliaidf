[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

# Home Assistant - Veolia IDF integration

Fetch Veolia IDF data to Home Assistant sensor.

## Installation

You can install this integration with [HACS](https://hacs.xyz/) by adding
a custom repository.

Or you can copy the folder `custom_components/veoliaidf` into your
configuration folder (not recommended).

When it is installed, you can add the integration in the Home Assistant
configuration part, and your credentials will be asked.

## Requirement

This integration is based on [PyVeoliaIDF](https://github.com/ssenart/PyVeoliaIDF)
python library to get the data. This library is working with Selenium Python library
and needs a Mozilla Web Driver.

Mozilla Geckodriver can be build using the repository:
[geckodriver-build](https://github.com/valletw/geckodriver-build)

## Configuration

The configuration is done in the UI. The YAML configuration is deprecated.
