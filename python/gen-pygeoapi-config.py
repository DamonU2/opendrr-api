import json
import configparser

from elasticsearch import Elasticsearch
from elasticsearch import helpers

#Main Function
def main():

    auth = get_config_params('config.ini')

    # es = Elasticsearch()
    es = Elasticsearch([auth.get('es', 'es_endpoint')],
                       http_auth=(auth.get('es', 'es_un'),
                                  auth.get('es', 'es_pw')))

    config = """# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#
# Copyright (c) 2020 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

server:
    bind:
        host: 0.0.0.0
        port: 5000
    url: http://localhost:5000
    mimetype: application/json; charset=UTF-8
    encoding: utf-8
    language: en-US
    # cors: true
    pretty_print: true
    limit: 10
    # templates:
      # path: /path/to/Jinja2/templates
      # static: /path/to/static/folder # css/js/img
    map:
        url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png'
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors, Points &copy 2012 LINZ'
        # url: https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png
        # attribution: '<a href="https://wikimediafoundation.org/wiki/Maps_Terms_of_Use">Wikimedia maps</a> | Map data &copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
#    manager:
#        name: TinyDB
#        connection: /tmp/pygeoapi-process-manager.db
#        output_dir: /tmp/
    # ogc_schemas_location: /opt/schemas.opengis.net

# logging:
    level: ERROR
    logfile: /tmp/pygeoapi.log

metadata:
    identification:
        title: pygeoapi default instance
        description: pygeoapi provides an API to geospatial data
        keywords:
            - geospatial
            - data
            - api
        keywords_type: theme
        terms_of_service: https://creativecommons.org/licenses/by/4.0/
        url: http://example.org
    license:
        name: CC-BY 4.0 license
        url: https://creativecommons.org/licenses/by/4.0/
    provider:
        name: Organization Name
        url: https://pygeoapi.io
    contact:
        name: Lastname, Firstname
        position: Position Title
        address: Mailing Address
        city: City
        stateorprovince: Administrative Area
        postalcode: Zip or Postal Code
        country: Country
        phone: +xx-xxx-xxx-xxxx
        fax: +xx-xxx-xxx-xxxx
        email: you@example.org
        url: Contact URL
        hours: Mo-Fr 08:00-17:00
        instructions: During hours of service. Off on weekends.
        role: pointOfContact

resources:\n\n"""

    snippet = """{0}:
        type: collection
        title: {1}
        description: {2}
        keywords:
            - earthquake
        links:
            - type: text/html
              rel: canonical
              title: information
              href: http://www.riskprofiler.ca/
              hreflang: en-US
        extents:
            spatial:
                bbox: [-180,-90,180,90]
                crs: http://www.opengis.net/def/crs/OGC/1.3/CRS84
            temporal:
                begin: 2020-08-06
                end: null  # or empty (either means open ended)
        providers:
            - type: feature
              name: Elasticsearch
              data: """ + auth.get('es', 'es_endpoint') + """/{3}
              id_field: {4}"""

    text_file = open("pygeoapi_config.txt", "w")

    id_field = "AssetID"

    for index in es.indices.get('*'):
        if (index[0] == '.'):
            continue

        if index[-2:] == "_s":
            id_field = "Sauid" 

        config += "    " +snippet.format(index, index, index, index, id_field) + "\n\n"

    text_file.write(config)
    text_file.close()

def get_config_params(args):
    """
    Parse Input/Output columns from supplied *.ini file
    """
    configParseObj = configparser.ConfigParser()
    configParseObj.read(args)
    return configParseObj



if __name__ == '__main__':
    main() 