#!/bin/bash

DELAY=25

mongo <<EOF
var config = {
    "_id": "rs",
    "version": 1,
    "members": [
        {
            "_id": 1,
            "host": "mongo1:27017",
            "priority": 2
        },
        {
            "_id": 2,
            "host": "mongo2:27017",
            "priority": 1
        }
    ]
};
rs.initiate(config, { force: true });
EOF

echo "############# initiating replica set #############"
echo "creating users..."
sleep $DELAY

mongo < /scripts/init.js
echo "users created!"
echo "############# replica set initiated #############"