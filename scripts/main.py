import sys
import json
import requests

def main(event):
    print("Event data:", event)

if __name__ == "__main__":
    print("Entrou aqui")
    event_data = json.loads(sys.stdin.read())
    main(event_data)