import os
import open3d.ml as _ml3d
import open3d.ml.tf as ml3d
from open3d.ml.vis import Visualizer, BoundingBox3D, LabelLUT
from open3d.ml.tf.dataloaders import TFDataloader as Dataloader
import sys
from pathlib import Path
import pprint
import numpy as np

from ouster import client, pcap
from contextlib import closing
from more_itertools import nth

pcap_path = '/home/daniel.sohn/Desktop/KITTI_DATASET/OS1_128_sample/OS1_128.pcap'
metadata_path = '/home/daniel.sohn/Desktop/KITTI_DATASET/OS1_128_sample/OS1_2048x10_128.json'

with open(metadata_path, 'r') as f:
        metadata = client.SensorInfo(f.read())

source = pcap.Pcap(pcap_path, metadata)

with closing(client.Scans(source)) as scans:
        scan = nth(scans, 200) #200

xyzlut = client.XYZLut(source.metadata)

#destagger
signal  = client.destagger(metadata,scan.field(client.ChanField.REFLECTIVITY))
signal = (signal / np.max(signal)).astype(np.float32)
xyz_destaggered = client.destagger(metadata, xyzlut(scan))
[x, y, z] = [c.flatten() for c in np.dsplit(xyz_destaggered, 3)]
signal = signal.flatten()

#-138.7421970539727
#-134.58247301252425
#-3.706122761506571
#101.08938228465978
#144.26862948978524
#14.637696552581591
point_cloud = np.asarray([x,y,z,signal], dtype =  np.float32).transpose()


#AND NOW TO PT_PILLAR
cfg_file = "/home/daniel.sohn/Desktop/point_pillars/Open3D-ML/ml3d/configs/pointpillars_kitti.yml"

cfg = _ml3d.utils.Config.load_from_file(cfg_file)

model = ml3d.models.PointPillars(**cfg.model)

cfg.dataset['dataset_path'] = "/home/daniel.sohn/Desktop/KITTI_DATASET/KITTI_PTCLOUD_DATA/data_object_velodyne"
#DSOHN: LOOKS LIKE USING CUSTOM DATASET.PY  FOR OUSTER IS NEEDED
dataset = ml3d.datasets.KITTI(cfg.dataset.pop('dataset_path', None), **cfg.dataset)
#pipeline = ml3d.pipelines.ObjectDetection(model, dataset=dataset, device="gpu", **cfg.pipeline)
pipeline = ml3d.pipelines.ObjectDetection(model, device="gpu", **cfg.pipeline)

ckpt_path = '/home/daniel.sohn/Desktop/KITTI_DATASET/pointpillars_kitti_202012221652utc/ckpt-12'

# load the parameters.
pipeline.load_ckpt(ckpt_path=ckpt_path)

#points = point_cloud #get stuff from ouster [x,y,z,i]

data = {
            'point': point_cloud,
            'full_point': point_cloud,
            'feat': None,
            'calib': None,
            'bounding_boxes': [],
        }

result = pipeline.run_inference(data)

print(result)

box_list = result[0]
bbox_list=[]
for box in box_list:
    pos = box[0]
    dim = box[1]
    yaw = box[2]
    name = box[3]
    score = box[4]
    print(name)
    print(score)
    bbox = BoundingBox3D(center = pos, front = (np.sin(yaw),np.cos(yaw),0), left = (np.cos(yaw),-np.sin(yaw),0) , up = (0,0,1),  size = dim, label_class=name, confidence = score,show_class = True,show_confidence = True)
    bbox_list.append(bbox)

lut = LabelLUT()
lut.add_label(0,0,[1,0,0])
#lut.add_label('Pedestrian',0,[1,0,0])
lut.add_label(1,1,[1,0,0])
#lut.add_label('Cyclist',1,[1,0,0])
lut.add_label(2,2,[0,0,1])
#lut.add_label('Cars',2,[0,0,1])

vis = Visualizer()
vis.set_lut('labels',lut)

render_data = [{'name': 'OS1 point pillars', 'points': data['point']}]


vis.visualize(render_data,lut,bbox_list)







