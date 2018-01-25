#/bin/bash

ssh -A int.faktisk.no 'cd /apps/claimreview-scraper && git pull --ff-only origin master && cd viewer && yarn install && NODE_ENV=production PUBLIC_URL=/claimreviews yarn run build'