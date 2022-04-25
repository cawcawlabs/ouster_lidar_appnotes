import argparse
import os
import threading

import ouster.client as client
from ouster.sdk._viz import PyViz
import matplotlib.pyplot as plt
import numpy as np


#ouster safety designer imports
from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.ops import unary_union
from shapely.geometry import LineString
from shapely import affinity
import xml.etree.ElementTree as ET


def generate_sector(center, start_angle, end_angle, radius, steps=2048):
    def polar_point(origin_point, angle,  distance):
        return [origin_point.x + np.cos(np.radians(angle)) * distance, origin_point.y + np.sin(np.radians(angle)) * distance]
    if start_angle > end_angle:
        start_angle = start_angle - 360
    else:
        pass
        #print(start_angle, end_angle)
    step_angle_width = (end_angle-start_angle) / steps
    sector_width = (end_angle-start_angle) 
    segment_vertices = []

    segment_vertices.append(polar_point(center, 0,0))
    segment_vertices.append(polar_point(center, start_angle,radius))

    for z in range(1, steps):
        segment_vertices.append((polar_point(center, start_angle + z * step_angle_width,radius)))
    segment_vertices.append(polar_point(center, start_angle+sector_width,radius))
    segment_vertices.append(polar_point(center, 0,0))
    return Polygon(segment_vertices)

def process_geometry(single_field, zone_list):
    for geometry in single_field[:]:
        print(geometry.tag, geometry.attrib)
        if geometry.tag == 'Polygon':
            polygon_points=[]
            for point in geometry[:]:
                polygon_points.append([int(point.attrib['X']),int(point.attrib['Y'])]) 
            zone_list.append(Polygon(polygon_points))
        elif geometry.tag == 'CircleSector':
            center = Point(int(geometry.attrib['CenterX']), int(geometry.attrib['CenterY']))
            sect = generate_sector(center, start_angle = float(geometry.attrib['StartAngle']), end_angle = float(geometry.attrib['EndAngle']), radius = int(geometry.attrib['Radius']))
            #circle = Point(int(geometry.attrib['CenterX']), int(geometry.attrib['CenterY'])).buffer(int(geometry.attrib['Radius']))
            #circle.buffer(int(geometry.attrib['Radius']))
            zone_list.append(sect)
        else: 
            print('not processing this one')
    return zone_list
    
def parse_xml():
    mytree = ET.parse('/home/daniel.sohn/Desktop/range_envelope/safety_designer_output/field_set_demo.sdxml')
    myroot = mytree.getroot()
    protection_zone =[]
    warning_zone=[]
    for fieldset in myroot[2]:
        #[2] is for <Fieldsets>/field/geometry
        for field in fieldset[:]:
            print(field.tag, field.attrib)
            if field.attrib['Fieldtype'] == 'WarningSafeBlanking':
                warning_zone = process_geometry(field, warning_zone)
            elif field.attrib['Fieldtype'] == 'ProtectiveSafeBlanking':
                protection_zone = process_geometry(field, protection_zone)
            else:
                print('detected 3rd category field, not processing this one')
    warning_set = unary_union(warning_zone)
    protection_set = unary_union(protection_zone)


    #implement radial intersection, (0,0), 360 deg, 2048 resolution
    warning_mask=[]
    protection_mask=[]
    for theta in np.linspace(0,2*np.pi, num = 2048, endpoint=False):
        max_range = 900000 #max range of ouster detection
        radial_line = LineString([(0, 0), (max_range*np.cos(theta),max_range*np.sin(theta) )])

        warning_range = warning_set.intersection(radial_line).length
        protection_range = protection_set.intersection(radial_line).length
        
        warning_mask.append(warning_range) #warning envelope, plug in 2048x10 lidar mode
        protection_mask.append(protection_range) #protection envelope, plug in 2048x10 lidar mode
    
    return warning_mask, protection_mask
    
def main() -> None:
    descr = """Visualize pcap or sensor data using simple viz bindings."""

    epilog = """When reading data from a sensor, this will autoconfigure the udp
        destination unless -x is used."""

    parser = argparse.ArgumentParser(
        description=descr, epilog=epilog)

    required = parser.add_argument_group('one of the following is required')
    group = required.add_mutually_exclusive_group(required=True)
    group.add_argument('--sensor', metavar='HOST', help='sensor hostname')
    group.add_argument('--pcap', metavar='PATH', help='path to pcap file')

    parser.add_argument('--meta', metavar='PATH', help='path to metadata json')
    parser.add_argument('--lidar-port', type=int, help='lidar port for sensor')
    parser.add_argument('-x', '--no-auto-dest', help="""do not auto configure udp
        destination', action='store_true""")

    args = parser.parse_args()

    if args.sensor:
        hostname = args.sensor
        if args.lidar_port or (not args.no_auto_dest):
            config = client.SensorConfig()
            if args.lidar_port:
                config.udp_port_lidar = args.lidar_port
            print("Configuring sensor...")
            client.set_config(hostname, config, udp_dest_auto= (not args.no_auto_dest))
        config = client.get_config(hostname)

        print("Initializing...")
        scans = client.Scans.stream(hostname,
                                    config.udp_port_lidar or 7502,
                                    complete=True)

    elif args.pcap:
        import ouster.pcap as pcap

        if args.meta:
            metadata_path = args.meta
        else:
            print("Deducing metadata based on pcap name. "
                  "To provide a different metadata path, use --meta")
            metadata_path = os.path.splitext(args.pcap)[0] + ".json"

        with open(metadata_path) as json:
            info = client.SensorInfo(json.read())

        scans = client.Scans(
            pcap.Pcap(args.pcap, info, rate=1.0))
    
    viz = PyViz(scans.metadata)
    
    warning_mask, protection_mask = parse_xml()
    
    #ping = gTTS(text="PING!", lang='en', slow=False)
    #ping.save("ping.mp3")
    

    def run() -> None:
        try:
            for scan in scans:
                range_field = scan.field(client.ChanField.RANGE)
                range_img = client.destagger(scans.metadata, range_field)
                theta = np.linspace(0, 2*np.pi, num=2048)
                #r = np.amin(range_img, axis=0)/1000 #in meters, smallest range
                range_img[range_img<300] = -1
                #128 beams -> 64 is middle
                #0:2048
                #picking middle 3 beams
                r = np.amin(range_img[63:65,:], axis=0)#/1000 #aximuth and watch sector
                #insert mask switching, comparison here!
                #compare twice: warning and protection
                
                #flipping to match coordinates.....
                if(np.any([r<np.flip(protection_mask)])):
                    print("PROTECT!")
                    print("\a") #beep
                elif (np.any([r<np.flip(warning_mask)])): #did not trigger protect but still within warning
                    print("warning!")
                else:
                    print("clear")
                #colors = theta 
                #fig = plt.figure()
                #ax = fig.add_subplot(projection='polar')
                #ax.set_ylim([0,10])
                #c = ax.scatter(theta, r, c=colors, cmap='hsv', alpha=0.75)
                viz.draw(scan)
        finally:
            # signal main thread to exit
            viz.quit()

    try:
        print("Starting client thread...")
        client_thread = threading.Thread(target=run, name="Client")
        client_thread.start()

        print("Starting rendering loop...")
        viz.loop()
    finally:
        scans.close()
        client_thread.join()

    print("Done")


if __name__ == "__main__":
    main()

