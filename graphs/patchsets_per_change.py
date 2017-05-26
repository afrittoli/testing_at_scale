# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import sys

PROJECTS = set(['openstack/nova', 'openstack/neutron', 'openstack/keystone',
                'openstack/glance', 'openstack/cinder', 'openstack/swift',
                'openstack/tempest', 'openstack-dev/devstack'])

BASE_URL = 'https://review.openstack.org'
CHANGES_PATH = '/changes/'
CHANGES_PARAMS = dict(n=1000, o='ALL_REVISIONS')
CHANGES_QUERY = 'project: {project} status: merged'


def get_patchset_numbers():
    changes = dict()
    for project in PROJECTS:
        # Get a list of merged changes for that project
        query = CHANGES_QUERY.format(project=project)
        params = dict(CHANGES_PARAMS, query=query)
        response = requests.get(BASE_URL+CHANGES_PATH,
                                params=params)
        data = json.loads(response.text[len(')]}\''):])
        changes[project] = [len(x['revisions']) for x in data]
    return changes


def plot_histogram(labels, data):
    series = pd.Series(data, index=labels)
    title = 'Average number of patchset (last 1000 changes)'
    plot = series.plot(kind='bar', stacked=False).set_title(title)
    plt.tight_layout()
    fig = plot.get_figure()
    fig.savefig('patchsets_per_change.png')


def main()::
    data = get_patchset_numbers()
    labels = [x.split("/")[1] for x in data]
    data_points = [np.mean(data[x]) for x in data]
    plot_histogram(labels, data_points)

if __name__ == "__main__":
    sys.exit(main())
