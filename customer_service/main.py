#!/usr/bin/env python3
import os, sys, time
from broker_comunication import broker_requests_handling_loop


def main():
    print("Customer SERIVCE STARTED")

    # time.sleep(5)
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
