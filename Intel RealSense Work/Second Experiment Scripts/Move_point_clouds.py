import copy
import open3d as o3d
import numpy as np

_30_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second Experiment Scripts\filtered_data\_30_pcd_filtered.ply")
_60_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second Experiment Scripts\filtered_data\_60_pcd_filtered.ply")
_90_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second Experiment Scripts\filtered_data\_90_pcd_filtered.ply")
_120_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second Experiment Scripts\filtered_data\_120_pcd_filtered.ply")
_150_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second Experiment Scripts\filtered_data\_150_pcd_filtered.ply")
_180_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second Experiment Scripts\filtered_data\_180_pcd_filtered.ply")
_210_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second Experiment Scripts\filtered_data\_210_pcd_filtered.ply")
_240_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second Experiment Scripts\filtered_data\_240_pcd_filtered.ply")
_270_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second Experiment Scripts\filtered_data\_270_pcd_filtered.ply")
_300_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second Experiment Scripts\filtered_data\_300_pcd_filtered.ply")
_330_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second Experiment Scripts\filtered_data\_330_pcd_filtered.ply")
_360_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second Experiment Scripts\filtered_data\_360_pcd_filtered.ply")

#o3d.visualization.draw_geometries(
#         [_30_pcd, _60_pcd, _90_pcd, _120_pcd,_150_pcd,_180_pcd,_210_pcd,_240_pcd,_270_pcd,_300_pcd,_330_pcd, _360_pcd])


#Two translation on the x for automation 
# pie/6 is 30 degrees, how much we would have to rotate. 

#rotate all pcd's pie/6 counterclockwise?

#rotate 30-90

#Always copy before rotates and translations it will affect the pcd forever and can cause weird issues running over and over.



_180_temp = copy.deepcopy(_180_pcd)
matrix_transform_180_ = _90_pcd.get_rotation_matrix_from_xyz((0 ,np.pi/2,0))
_180_temp = _180_temp.rotate(matrix_transform_180_, center=(0,0,0))
_180_temp = _180_temp.translate((0.49,0,-0.44))


_270_temp = copy.deepcopy(_270_pcd)
matrix_transform_270 = _90_pcd.get_rotation_matrix_from_xyz((0 ,np.pi,0))
_270_temp = _270_temp.rotate(matrix_transform_270, center=(0,0,0))
_270_temp = _270_temp.translate((0.04,-0.02,-0.94))

_360_temp = copy.deepcopy(_360_pcd)
matrix_transform_360 = _90_pcd.get_rotation_matrix_from_xyz((0 , (3* np.pi)/2,0))
_360_temp = _360_temp.rotate(matrix_transform_360, center=(0,0,0))
_360_temp = _360_temp.translate((-0.42,-0.02,-0.5))

#Visualize

o3d.visualization.draw_geometries(
         [_90_pcd,_180_temp,_270_temp,_360_temp])


#add all transformed pcd's

combined_pcd = o3d.geometry.PointCloud()
combined_pcd += _90_pcd
combined_pcd += _180_temp
combined_pcd += _270_temp
combined_pcd += _360_temp

#Write to system below

#o3d.io.write_point_cloud(r"Intel RealSense Work\Second Experiment Scripts\filtered_data\combined_filtered_toy_car.ply", combined_pcd)








# MISC --------------------------------------- IGNORE

#How to add to first column of numpy array.
#back_pcd_as_array[:,0]+=0.3e

#Display each value in the first column of the numpy array
#for i in back_pcd_as_array[ :,1]:
    #print(i)
    #i[...] = i + x_change

# # Pass numpy array to Open3D.o3d.geometry.PointCloud and visualize
# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(back_pcd_as_array)
# o3d.io.write_point_cloud(r"C:\Users\Brien\Desktop\jupyterWork\MY PROJECTS\Intel RealSense\data\toy_car.ply", pcd)

# #Load in new point cloud.
# new_back_pcd = o3d.io.read_point_cloud(r"C:\Users\Brien\Desktop\jupyterWork\MY PROJECTS\Intel RealSense\data\toy_car.ply")
# side_pcd.paint_uniform_color([1, 0.706, 1])
# back_pcd.paint_uniform_color([0, 0.651, 0.929])
# o3d.visualization.draw_geometries([side_pcd])
