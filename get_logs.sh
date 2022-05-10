#!/bin/bash
#sudo docker service logs RSWW_172127_customer
sudo docker service logs RSWW_172127_api_gateway
sudo docker service logs RSWW_172127_broker
sudo docker service logs RSWW_172127_order
sudo docker service logs RSWW_172127_customer
sudo docker service logs RSWW_172127_offer
sudo docker service logs RSWW_172127_payment
sudo docker service logs RSWW_172127_web
