#!/bin/bash

FONT_SIZE=24

# Get the zuul all_jobs graph
curl "http://graphite.openstack.org/render/?from=-24hours&height=800&width=1024&until=now&bgcolor=ffffff00&fgcolor=000000&hideLegend=True&areaMode=first&fontSize=$FONT_SIZE&target=color(smartSummarize(sumSeries(stats_counts.zuul.pipeline.*.all_jobs),'1h'),'950004')&target=color(lineWidth(dashed(movingAverage(summarize(sumSeries(stats_counts.zuul.pipeline.*.all_jobs),'1h'),24)),6),'007BA7')&title=Zuul%20Jobs%20Launched%20(per%20Hour)&hideGrid=true&xFormat=%I%p&margin=40" > zuul_all_jobs.png
