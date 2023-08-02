## The Splainer!

This is a version of [Splainer](http://github.com/o19s/splainer) that allows running via Solr Admin UI as a Solr Plugin!.

<img width="395" alt="image" src="https://github.com/epugh/solr-splainer/assets/629060/5aac89f7-d37a-48c9-9416-533fe22ec88b">

## Building and installation

With [npm installed](https://www.npmjs.com/)

```bash
npm install -g grunt-cli
npm install .
grunt dist
$ (cd dist && zip -r - *) > splainer.zip
unzip splainer.zip -d ~/path/to/solr/server/solr-webapp/webapp/splainer
```

See [main Splainer project](http://github.com/o19s/splainer) for more project information

### Changes to make it work in Solr Admin UI

See [diff from main project](https://github.com/o19s/splainer/compare/main...softwaredoug:solr-splainer:main#diff-18e01ac6a833fb1b20ffbad54f0ad8834a765e766f72cccda1e56cb942864d25R30)

* Changes communication with Solr to use GET instead af JSONP, same way the Admin UI communicates with Solr

1. Export the private key:

```export SOLR_PACKAGE_SIGNING_PRIVATE_KEY_PATH=~/.solr-private-key.pem```

2. Build the package:

```mvn package```

3. Now, host the solr-splainer-plugin/repo folder:

```cd solr-splainer-plugin; python -m http.server```

4. In a Run Solr and install the package:

    tar -xf solr-9.3.0.tgz; cd solr-9.3.0/
    bin/solr start -c -Denable.packages=true;
    bin/solr package add-repo splainer-repo "http://localhost:8000/repo/"; 
    bin/solr package list-available; 
    bin/solr package install solr-splainer; 
    bin/solr package deploy solr-splainer -y -cluster

5. Navigate to http://localhost:8983/v2/splainer on the browser.


## Who?

Another Hack by [Doug Turnbull](http://softwaredoug.com)

Created by [OpenSource Connections](http://opensourceconnections.com).

Thanks to all the [community contributors](https://github.com/o19s/splainer/graphs/contributors) for finding bugs and sharing fixes!.

## License

Released under [Apache 2](LICENSE.txt)
