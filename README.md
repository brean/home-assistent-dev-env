# Home assistent development environment

Docker based home assistent development environment to create Hass-Components (travis-ci for integration testing).

[![Build Status](https://travis-ci.org/brean/home-assistent-dev-env.svg?branch=master)](https://travis-ci.org/brean/home-assistent-dev-env)

## Overview

This system consists of 4 docker container:

- **home_assistant** container for a home assistant instance
- **nginx** a webserver to allow access to home-assistant from the host system.
- **mqtt** a mosquitto-server (unused for now, but might be useful in the future).
- **testing** runs the unit-tests in a headless Chrome browser using selenium so we can write unit-tests to veryfiy the data get received by home-assistant.

## Usage

This example system tests the integration of a simple sensor into home-assistant by veryfing its shown in the loveace-ui. The code for this is based on <https://github.com/home-assistant/example-custom-config/tree/master/custom_components/example_sensor> its code can be found in `example_sensor/` which is mounted to `/config/custom_components/example_sensor` in the `docker-compose.yml`-file

## Manual-testing

Run `docker-compose up home_assistant` to start home-assistant behind nginx and mqtt as development setup.

The home-assistant config comes with a user for the web interface named `user`, his password is `1234`.

You can access the web interface for manual testing on [http://localhost](http://localhost), assuming you havn't changed anything and run nginx on port 80 - feel free to change that in the `docker-compose.yml`.

It also includes a basic setup of MQTT using an own mosquitto instance.

## Integration-Testing

to run the integration tests just run `docker-compose run testing`.

This will also be run by travis - take a look at the `.travis-ci.yml` for details.
