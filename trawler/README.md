# trawler

A utility to trawl phishing domains and attempt to identify phishing kits as well as other malicious activity

## Configuration Options

In order to trawl provided websites you must specify the database connection (leave as is unless you understand what is happening).

```yaml
database:
    server: mongo
    port: 27017
    name: chum
    collection: trawl
```

Next, you can specify the extensions which you want to download if found on the web server.  Additionally, you can specify an alternate folder path to store these kits.

```yaml
download:
    extensions: 
        - zip
        - exe
        - msi
        - mp4
        - ps1
        - txt
        - log
        - apk
        - dll
        - bin
    folder: kits
```