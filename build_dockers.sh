#!/bin/bash
set -e

docker build . -f api_gateway/Dockerfile -t leckijakub/rsww_172127_api_gateway -t 10.40.71.55:5000/rsww_172127_api_gateway
docker build . -f broker_service/Dockerfile -t leckijakub/rsww_172127_broker -t 10.40.71.55:5000/rsww_172127_broker
docker build . -f order_service/Dockerfile -t leckijakub/rsww_172127_order -t 10.40.71.55:5000/rsww_172127_order
docker build . -f customer_service/Dockerfile -t leckijakub/rsww_172127_customer -t 10.40.71.55:5000/rsww_172127_customer
docker build . -f offer_service/Dockerfile -t leckijakub/rsww_172127_offer -t 10.40.71.55:5000/rsww_172127_offer
docker build . -f payment_service/Dockerfile -t leckijakub/rsww_172127_payment -t 10.40.71.55:5000/rsww_172127_payment
docker build . -f web_service/Dockerfile -t leckijakub/rsww_172127_web -t 10.40.71.55:5000/rsww_172127_web


docker push leckijakub/rsww_172127_api_gateway
docker push leckijakub/rsww_172127_broker
docker push leckijakub/rsww_172127_order
docker push leckijakub/rsww_172127_customer
docker push leckijakub/rsww_172127_offer
docker push leckijakub/rsww_172127_payment
docker push leckijakub/rsww_172127_web
