#!/bin/bash
set -e

docker build . -f api_gateway/Dockerfile -t leckijakub/rsww_172127_api_gateway:1.0 -t 10.40.71.55:5000/rsww_172127_api_gateway
docker build . -f broker_service/Dockerfile -t leckijakub/rsww_172127_broker:1.0 -t 10.40.71.55:5000/rsww_172127_broker
docker build . -f order_service/Dockerfile -t leckijakub/rsww_172127_order:1.0 -t 10.40.71.55:5000/rsww_172127_order
docker build . -f customer_service/Dockerfile -t leckijakub/rsww_172127_customer:1.0 -t 10.40.71.55:5000/rsww_172127_customer
docker build . -f offer_service/Dockerfile -t leckijakub/rsww_172127_offer:1.0 -t 10.40.71.55:5000/rsww_172127_offer
docker build . -f payment_service/Dockerfile -t leckijakub/rsww_172127_payment:1.0 -t 10.40.71.55:5000/rsww_172127_payment
docker build . -f web_service/Dockerfile -t leckijakub/rsww_172127_web:1.0 -t 10.40.71.55:5000/rsww_172127_web


docker push leckijakub/rsww_172127_api_gateway:1.0
docker push leckijakub/rsww_172127_broker:1.0
docker push leckijakub/rsww_172127_order:1.0
docker push leckijakub/rsww_172127_customer:1.0
docker push leckijakub/rsww_172127_offer:1.0
docker push leckijakub/rsww_172127_payment:1.0
docker push leckijakub/rsww_172127_web:1.0
