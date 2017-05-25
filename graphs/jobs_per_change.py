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

import pandas as pd
import numpy as np
from oslo_config import cfg
from sqlalchemy import func
from sqlalchemy.orm import aliased
from subunit2sql.db import api
from subunit2sql.db import models
from subunit2sql import shell
import sys


CONF = cfg.CONF
CONF.import_opt('verbose', 'subunit2sql.db.api')

PROJECTS = set(['openstack/nova', 'openstack/neutron', 'openstack/keystone',
                'openstack/glance', 'openstack/cinder', 'openstack/swift',
                'openstack/tempest', 'openstack-dev/devstack'])


def get_jobs_per_project(session=None):
    session = session or api.get_session()
    rm_build_change = aliased(models.RunMetadata)
    rm_build_patchset = aliased(models.RunMetadata)
    rm_project = aliased(models.RunMetadata)
    select_query = session.query(
        rm_build_change.value.label('build_change'),
        rm_build_patchset.value.label('build_patchset'),
        rm_project.value.label('project'),
        func.count().label('num_jobs')
    ).select_from(rm_build_change)
    all_run_metadata_query = select_query.filter(
        rm_build_change.run_id == rm_build_patchset.run_id).filter(
        rm_project.run_id == rm_build_patchset.run_id).filter(
        rm_build_change.key == 'build_change').filter(
        rm_build_patchset.key == 'build_patchset').filter(
        rm_project.key == 'project').filter(
        rm_project.value.in_(PROJECTS)).group_by(
            rm_build_change.value,
            rm_build_patchset.value,
            rm_project.value)
    result = dict()
    all_data = all_run_metadata_query.all()
    for change, patchset, project, num_jobs in all_data:
        if project not in result:
            result[project] = dict()
        change_patchset = change + ":" + patchset
        result[project][change_patchset] = int(num_jobs)
    return result


def get_job_counts_per_change(change, patchset, session=None):
    session = session or api.get_session()
    rm_build_change = aliased(models.RunMetadata)
    rm_build_patchset = aliased(models.RunMetadata)
    rm_build_name = aliased(models.RunMetadata)
    select_query = session.query(
        rm_build_name.value.label('build_name'),
        func.count().label('job_counts')
    ).select_from(rm_build_change)
    all_run_metadata_query = select_query.filter(
        rm_build_change.run_id == rm_build_patchset.run_id).filter(
        rm_build_name.run_id == rm_build_patchset.run_id).filter(
        rm_build_change.key == 'build_change',
        rm_build_change.value == change).filter(
        rm_build_patchset.key == 'build_patchset',
        rm_build_patchset.value == patchset).filter(
        rm_build_name.key == 'build_name').group_by(
            rm_build_change.value,
            rm_build_patchset.value,
            rm_build_name.value)
    result = dict()
    all_data = all_run_metadata_query.all()
    for build_name, job_counts in all_data:
        result[build_name] = int(job_counts)
    return result


def plot_histogram(labels, data):
    series = pd.Series(data, index=labels)
    title = 'Average gate jobs per project'
    plot = series.plot(kind='bar', stacked=False).set_title(title)
    fig = plot.get_figure()
    fig.savefig('gate_jobs.png')


def main():
    shell.parse_args(sys.argv)
    session = api.get_session()
    project_data = get_jobs_per_project(session)
    averages = []
    for project in project_data:
        changes = project_data[project]
        values = list(changes.values())
        averages.append(np.mean(values))

    labels = [x.split("/")[1] for x in project_data]
    plot_histogram(labels, averages)


if __name__ == "__main__":
    sys.exit(main())
