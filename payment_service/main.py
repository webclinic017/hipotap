#!/usr/bin/env python3
import os
import sys

from broker_comunication import broker_requests_handling_loop

def main():
    print("Payment SERIVCE STARTED")

    broker_requests_handling_loop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
