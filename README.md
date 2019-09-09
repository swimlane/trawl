# trawl

A set of utilities used to assist with identify potential phishing websites and downloading potentially malicious content.

# THIS PROJECT CURRENTLY UNDER DEVELOPMENT AND IT NOT READY FOR TESTING.  PLEASE STAR OR WATCH THIS PROJECTS FOR FUTURE UPDATES AS I CONTINUE TO UPDATE IT

## About

You can find more information about this tool during my presentation at DerbyCon 2019. Please visit my [blog](https://letsautomate.it/page/presentations/) for the slides and a link to the video.

### Services

`trawl` includes the following services (containers):

* [entrails](entrails/README.md) (MongoDB which contains 3 document models)
* [spotter](spotter/README.md) (spotter is used to spot potential malicious URLs)
* [trawler](trawler/README.md) (trawler is used to scrape websites for malicious content)
* Chum (chum is a RabbitMQ queue used by both spotter and trawler)


`trawl` is designed with Docker in mind and is catered towards rapid setup and deployment.  The general architecture can be seen below:

![trawl architecture](https://letsautomate.it/presentations/hunting-for-phishkits/0b7a46f66e919d54f4b03b7ddc8841e7.png)

## Requirements

* Docker-Compose

## Usage

To begin using `trawl` make sure you have docker and docker-compose installed on your system and then you must clone the repository:

```bash
git clone git@github.com:swimlane/trawl.git
```

change directories into the `trawl` folder and run

```bash
docker-compose up
```

This will begin creating and setting up all services.

