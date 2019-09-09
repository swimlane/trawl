# spotter

Spotter is a utility to retrieve potential URLs from multiple sources and add them to a Rabbit MQ queue.

## Current Supported Services

* [OpenPhish](https://openphish.com/)
* [Phishing.Database](https://github.com/mitchellkrogza/Phishing.Database)
* [PhishTank](https://www.phishtank.com/)
* [Twitter](https://twitter.com)
* [UrlScan](https://urlscan.io/)
* [WebAnalyzer](https://wa-com.com/)
* [WHOIS Domain search](https://whoisds.com/)

## Configuration

You must specify a configuration for any existing or new service added in the `spotter.yml` configuration file.

### Current Default Configuration

The following services have only a `check-interval` and `days` and `hours` configuration option:

* urlscan
* phishtank
* whoisds
* phishingdatabase
* openphish

```yaml
check-interval:
    days: 0
    hours: 2
```

#### WebAnalyzer

WebAnalyzer has a `check-interval` configuration but also a `tld` list configuration option as well.  Any TLDs added will be checked for when downloading latest domains from this service.  By default we have included all of their supported TLDs:


```yaml
webanalyzer:
  check-interval:
    days: 0
    hours: 2
  tld:
    - com
    - net
    - org
    - info
    - us
    - biz
    - cat
    - club
    - fun
    - life
    - live
    - ltd
    - pro
    - shop
    - store
    - tech
    - vip 
    - ...
```

#### Twitter

To scrape twitter you must register a application and provide your `check-interval` as well as hashtags you want to search for and your API keys.  Example is below:

```yaml
twitter:
  check-interval:
    days: 0
    hours: 2
  hashtags:
    - opendir
    - phishkit
    - phishingkit
  consumer_key: {CONSUMER_KEY}
  consumer_secret: {CONSUMER_SECRET}
  access_token_key: {ACCESS_TOKEN_KEY}
  access_token_secret: {ACCESS_TOKEN_SECRET}
```