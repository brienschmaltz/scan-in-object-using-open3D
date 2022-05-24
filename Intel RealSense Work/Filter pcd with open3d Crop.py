import open3d as o3d
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

front_pcd_filtered = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\filtered_front_pcd_final.ply")
back_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\180 degree.ply")
side_pcd= o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\90 degree.ply")
side2_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\270 degree.ply")
top_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\top_view.ply") 

#For reusability 
point_cloud = front_pcd_filtered

#For Dr. Reiman demonstration
#point_cloud = side2_pcd

print("Filter point cloud with regression line.")

bounding_box = point_cloud.get_axis_aligned_bounding_box()
bounding_box.color = (1,0,0)
dimensions = np.asarray(bounding_box.get_box_points())
print(dimensions)

#Edit box dimensions
sliced_dim = dimensions[0:4, :]
print("----------")

#Make new point cloud for adjusted bounding box
new_bb = o3d.geometry.PointCloud()
new_bb.points = o3d.utility.Vector3dVector(sliced_dim)
final_bb = bounding_box.create_from_points(new_bb.points)

# Scale bounding box from center
center = np.asarray(bounding_box.get_center())
print(center)
# make slight adjustments to center
#for side_pcd
#center[2]+=0.2
#center[1]+=0.07

center[2]+=0.3
center[1]-=0.28
center[0]-=0.4
bounding_box = bounding_box.scale(0.50, center)


#Create new point cloud from cropped original
cropped = point_cloud.crop(bounding_box)

print('Before bounding box crop')
o3d.visualization.draw(
         [point_cloud, bounding_box])

print('After bounding box crop')
o3d.visualization.draw(
         [cropped])

#Save
#o3d.io.write_point_cloud(r"data\Toy Truck PLY files\Filtered\Regression Filter\filtered_front_pcd_final.ply", cropped)