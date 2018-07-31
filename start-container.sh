#!/bin/bash

# the default node number is 2
N=${1:-3}

py


# get into hadoop master container
docker exec -it hadoop-master bash
