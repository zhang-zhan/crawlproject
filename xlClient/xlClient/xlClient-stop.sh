#!/bin/sh
ps -e | grep c_start|awk '{print $1}'|xargs kill -9
