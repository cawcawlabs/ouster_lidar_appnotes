import argparse
import os
import threading

import numpy as np

import ouster.client as client
from ouster.sdk._viz import PyViz


import open3d.ml as _ml3d
import open3d.ml.tf as ml3d
from open3d.ml.vis import Visualizer, BoundingBox3D, LabelLUT
from open3d.ml.tf.dataloaders import TFDataloader as Dataloader
import sys
from pathlib import Path
import pprint

from ouster import client, pcap
from contextlib import closing
from more_itertools import nth



#bbox item to translated pose matrix and others
def bbox2cuboid(box):
    pos = box[0] #(x,y,z)
    dim = box[1]
    yaw = box[2]
    name = box[3]
    score = box[4]
    print(name + ' '+ str(score))
    #no rotation for now. just position and size.... 
    pose = np.identity(4, dtype=np.dtype('float32'))
    pose[0, 3] = pos[0]  #x translate x + 2
    pose[1, 3] = pos[1]  #y
    pose[2, 3] = pos[2]  #z
    if name == "Car":
        rgba = np.array([1, 0, 0, score], dtype=np.dtype('float32')).T

    elif (name == "Pedestrian"):
        rgba = np.array([0, 1, 0, score], dtype=np.dtype('float32')).T

    elif (name == "Cyclist"):
        rgba = np.array([0, 0, 1, score], dtype=np.dtype('float32')).T

    else:
        rgba = np.array([0.5, 0.5, 0, 0], dtype=np.dtype('float32')).T

    #pose = np.identity(4, dtype=np.dtype('float32'))
    #rgba = np.array([1, 0, 0, 0], dtype=np.dtype('float32')).T
    #viz.add_cuboid(pose, rgba, "foobar")
    return pose, rgba, name

def main() -> None:

    #initialize ptpillar inference here
    #AND NOW TO PT_PILLAR
    cfg_file = "/home/daniel.sohn/Desktop/point_pillars/Open3D-ML/ml3d/configs/pointpillars_kitti.yml"
    cfg = _ml3d.utils.Config.load_from_file(cfg_file)
    model = ml3d.models.PointPillars(**cfg.model)
    cfg.dataset['dataset_path'] = "/home/daniel.sohn/Desktop/KITTI_DATASET/KITTI_PTCLOUD_DATA/data_object_velodyne"
    dataset = ml3d.datasets.KITTI(cfg.dataset.pop('dataset_path', None), **cfg.dataset)
    pipeline = ml3d.pipelines.ObjectDetection(model, device="gpu", **cfg.pipeline)
    ckpt_path = '/home/daniel.sohn/Desktop/KITTI_DATASET/pointpillars_kitti_202012221652utc/ckpt-12'
    # load the parameters.
    pipeline.load_ckpt(ckpt_path=ckpt_path)


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
        #DSOHN
        info = client.Sensor(hostname).metadata
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

    def run() -> None:
        try:
            for scan in scans:

                xyzlut = client.XYZLut(scans.metadata)
                #destagger
                signal  = client.destagger(scans.metadata,scan.field(client.ChanField.REFLECTIVITY))
                signal = (signal / np.max(signal)).astype(np.float32)
                xyz_destaggered = client.destagger(scans.metadata, xyzlut(scan))
                [x, y, z] = [c.flatten() for c in np.dsplit(xyz_destaggered, 3)]
                signal = signal.flatten()
                point_cloud = np.asarray([x,y,z,signal], dtype =  np.float32).transpose()
                data = {
                          'point': point_cloud,
                          'full_point': point_cloud,
                          'feat': None,
                          'calib': None,
                          'bounding_boxes': [],
                       }
                result = pipeline.run_inference(data)

                viz.draw(scan)

                box_list = result[0]
                bbox_list=[]
                for box in box_list:
                       #if box[3] == 'Pedestrian':
                       pose, rgba, name = bbox2cuboid(box)
                       viz.add_cuboid(pose,rgba,name)

                # then call this once per frame of data
                viz.cuboid_swap()
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


