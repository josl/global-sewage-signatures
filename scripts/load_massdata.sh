#!/usr/bin/env bash
#
# This script loads into a Redis database a file containing a list of Redis Protocol
# commands.

cat dataset/redis_protocol.txt | redis-cli -p 4444 --pipe
