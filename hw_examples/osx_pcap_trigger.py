
import logging
import threading
import time
from typing import Iterator, List, Union
import ouster.pcap as pcap
from datetime import datetime
from contextlib import closing
from ouster import client
from more_itertools import time_limited
from transitions import Machine

#global state machine "recorder"
class Recorder(object):
    pass
    
recorder = Recorder()


class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while not recorder.state == 'quit':
            self.input_cbk(input()) #waits to get input + Return

def keyboard_callback(inp):
    #evaluate the keyboard input
    if inp == 's':
        recorder.trigger('start_recording')
    elif inp == "":
        recorder.trigger('stop_recording') 
        if recorder.state == 'standby':   
            print('done with recording, standing by: (s)tart/(q)uit')
    elif inp == 'q':
        if recorder.state == 'recording':
            print('recording not finished. terminate with "enter" first')
        else:
            recorder.trigger('exiting')
    else:
        print('You Entered:', inp)


def _collect_indefinitely(sensor: client.Sensor) -> Iterator[client.Packet]:
    """Generator that uses a non-blocking thread to check for user input, then stops yielding packets"""
    print("Recording in progress: terminate with Enter key")
    packet_source = iter(sensor)
    while recorder.state == 'record':  # TODO: consider max time limit too
        yield next(packet_source)

hostname = 'os-992214000415.local'
lidar_port = 7502
imu_port = 7503
n_seconds = 30

def start_recording(source):
    
    # make a descriptive filename for metadata/pcap files
    time_part = datetime.now().strftime("%Y%m%d_%H%M%S")
    meta = source.metadata
    fname_base = f"/YOUR_SSD_PATH/{meta.prod_line}_{meta.sn}_{meta.mode}_{time_part}"
    #fname_base = f"{meta.prod_line}_{meta.sn}_{meta.mode}_{time_part}"

    print(f"Saving sensor metadata to: {fname_base}.json")
    source.write_metadata(f"{fname_base}.json")

    print(f"Writing to: {fname_base}.pcap (Ctrl-C to stop early)")
    #source_it = time_limited(n_seconds, source) from API example
    
    #source_it expires only when keyboard event occurs
    source_it = _collect_indefinitely(source)
    n_packets = pcap.record(source_it, f"{fname_base}.pcap")

    print(f"Captured {n_packets} packets")


if __name__ == "__main__":
    
    
    states=['standby', 'record', 'quit']
    
    transitions = [
    { 'trigger': 'start_recording', 'source': 'standby', 'dest': 'record' },
    { 'trigger': 'stop_recording', 'source': 'record', 'dest': 'standby' },
    { 'trigger': 'exiting', 'source': '*', 'dest': 'quit' },
    ]
    machine = Machine(model=recorder, states=states, transitions=transitions, initial='standby',ignore_invalid_triggers=True)
    
    #start the Keyboard thread
    kthread = KeyboardThread(keyboard_callback)
    with closing(client.Sensor(hostname, lidar_port, imu_port,
                               buf_size=640)) as source:
                               
        print("connected to sensor, standing by: (s)tart/(q)uit'")
        while True:
            if recorder.state == 'standby':
                pass
            elif recorder.state == 'record':
                print('recording!')
                start_recording(source)
            else: 
                recorder.state == 'quit'
                print('exiting')
                break
            
                
    
            
            
    
