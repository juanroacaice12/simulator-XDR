import time
import random
from threading import Thread
from queue import Queue

class Endpoint:
    def __init__(self, name, event_queue):
        self.name = name
        self.status = "Healthy"
        self.event_queue = event_queue

    def simulate_attack(self):
        attack_success = random.choice([True, False])
        if attack_success:
            self.status = "Compromised"
            self.event_queue.put((self.name, "Comprometido"))
        else:
            self.event_queue.put((self.name, "Seguro"))

class CentralServer:
    def __init__(self, event_queue):
        self.event_queue = event_queue

    def analyze_events(self):
        while True:
            endpoint_name, event_type = self.event_queue.get()
            if event_type == "Comprometido":
                print(f"ALERTA: Endpoint {endpoint_name} comprometido. Tomando medidas.")
            else:
                print(f"Endpoint {endpoint_name} seguro.")

def main():
    event_queue = Queue()

    central_server = CentralServer(event_queue)
    analysis_thread = Thread(target=central_server.analyze_events)
    analysis_thread.start()

    endpoint_names = ["Endpoint1", "Endpoint2", "Endpoint3"]
    endpoints = [Endpoint(name, event_queue) for name in endpoint_names]

    while True:
        for endpoint in endpoints:
            endpoint.simulate_attack()
            time.sleep(random.uniform(1, 5))

if __name__ == "__main__":
    main()
