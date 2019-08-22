This repo is for
https://github.com/helm/charts/tree/master/stable/elasticsearch
https://github.com/helm/charts/tree/master/stable/filebeat
https://github.com/helm/charts/tree/master/stable/metricbeat
https://github.com/helm/charts/tree/master/stable/kibana
https://github.com/helm/charts/tree/master/stable/kube-state-metrics

Changes to this repo are needed for StarlingX and those changes are
not yet merged.
Rather than clone and diverge the repo, the repo is extracted at a particular
git SHA, and patches are applied on top.

As those patches are merged, the SHA can be updated and
the local patches removed.
