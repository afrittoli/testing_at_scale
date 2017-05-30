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

import matplotlib.pyplot as plt
import os
import pandas as pd
import sys


def main():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    series = pd.read_csv(os.path.join(__location__, 'failure_rate.csv'),
                         index_col=0, parse_dates=[0])
    series.index.name = None
    title = 'Test failure rate over 5 months (1 day rolling average)'
    plot = series.plot(color=(0.58, 0, 0.01), legend=None,
                       ylim=(0, 100)).set_title(title)
    plt.tight_layout()
    fig = plot.get_figure()
    fig.savefig('failure_rate.png')


if __name__ == "__main__":
    sys.exit(main())
