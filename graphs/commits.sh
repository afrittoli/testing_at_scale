#!/bin/bash

# Get the commits graph
curl "http://graphite.openstack.org/render/?from=-500days&until=now&height=1200&width=1600&bgcolor=ffffff&fgcolor=000000&drawNullAsZero=true&target=movingAverage(summarize(stats_counts.gerrit.event.change-merged,'1d'),'60d')&target=movingAverage(summarize(stats_counts.gerrit.event.patchset-created,'1d'),'60d')&hideLegend=True&fontSize=22&&margin=40&areaMode=all" > commits.png
