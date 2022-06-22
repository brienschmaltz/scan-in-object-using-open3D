import copy
import open3d as o3d
import numpy as np

_30_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Second experiment Toy Truck PLY files\30 degree.ply")
_60_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Second experiment Toy Truck PLY files\60 degree.ply")
_90_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Second experiment Toy Truck PLY files\90 degree.ply")
_120_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Second experiment Toy Truck PLY files\120 degree.ply")
_150_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Second experiment Toy Truck PLY files\150 degree.ply")
_180_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Second experiment Toy Truck PLY files\180 degree.ply")
_210_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Second experiment Toy Truck PLY files\210 degree.ply")
_240_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Second experiment Toy Truck PLY files\240 degree.ply")
_270_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Second experiment Toy Truck PLY files\270 degree.ply")
_300_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Second experiment Toy Truck PLY files\300 degree.ply")
_330_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Second experiment Toy Truck PLY files\330 degree.ply")
_360_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Second experiment Toy Truck PLY files\360 degree.ply")

#o3d.visualization.draw_geometries(
#         [_30_pcd, _60_pcd, _90_pcd, _120_pcd,_150_pcd,_180_pcd,_210_pcd,_240_pcd,_270_pcd,_300_pcd,_330_pcd, _360_pcd])


#Two translation on the x for automation 
# pie/6 is 30 degrees, how much we would have to rotate. 

#rotate all pcd's pie/6 counterclockwise?

#rotate 30-90

#Always copy before rotates and translations it will affect the pcd forever and can cause weird issues running over and over.
# _60_temp = copy.deepcopy(_60_pcd)
# matrix_transform_60 = _30_pcd.get_rotation_matrix_from_xyz((0 ,np.pi/6,0))
# _60_temp = _60_temp.rotate(matrix_transform_60, center=(0,0,0))
# _60_temp = _60_temp.translate((0.37,0,-0.1))

# o3d.visualization.draw_geometries(
#          [_30_pcd,_60_temp])

# _90_temp = copy.deepcopy(_90_pcd)
# matrix_transform_90 = _30_pcd.get_rotation_matrix_from_xyz((0 ,np.pi/3,0))
# _90_temp = _90_temp.rotate(matrix_transform_90, center=(0,0,0))
# _90_temp = _90_temp.translate((0.40,0,-0.2))

# o3d.visualization.draw_geometries(
#          [_30_pcd,_90_temp])



_180_temp = copy.deepcopy(_180_pcd)
matrix_transform_180_ = _30_pcd.get_rotation_matrix_from_xyz((0 ,4.8* np.pi,0))
_180_temp = _180_temp.rotate(matrix_transform_180_, center=(0,0,0))
_180_temp = _180_temp.translate((0.3,0,-0.8))

o3d.visualization.draw_geometries(
         [_90_pcd,_180_temp])


# #180 ply rotation (front side)
# matrix_transform_1 = front_pcd.get_rotation_matrix_from_xyz((0 ,-0.5* np.pi,0))
# front_pcd = front_pcd.rotate(matrix_transform_1, center=(side_pcd_as_array[:,0].mean(),side_pcd_as_array[:,1].mean(),side_pcd_as_array[:,2].mean()))
# front_pcd = front_pcd.translate((-0.055,-0.02,-0.001))

# #270 ply rotation (left side)
# matrix_transform_2 = side2_pcd.get_rotation_matrix_from_xyz((0 ,1* np.pi,0))
# side2_pcd = side2_pcd.rotate(matrix_transform_2, center=(side_pcd_as_array[:,0].mean(),side_pcd_as_array[:,1].mean(),side_pcd_as_array[:,2].mean()))
# side2_pcd = side2_pcd.translate((-0.015,-0.02,0.004))

# #top rotation
# matrix_transform_3 = side2_pcd.get_rotation_matrix_from_xyz((-0.6* np.pi ,0,0))
# top_pcd = top_pcd.rotate(matrix_transform_3, center=(side_pcd_as_array[:,0].mean(),side_pcd_as_array[:,1].mean(),side_pcd_as_array[:,2].mean()))
# top_pcd = top_pcd.translate((0.01,0.12,0.1))

# #Bounding box and final display
# axis_aligned_bounding_box = side_pcd.get_axis_aligned_bounding_box()
# axis_aligned_bounding_box.color = (1, 0, 0)
# oriented_bounding_box = side_pcd.get_oriented_bounding_box()
# oriented_bounding_box.color = (0, 1, 0)
# print("Displaying axis_aligned_bounding_box in red and oriented bounding box in green ...")
# o3d.visualization.draw_geometries(
#          [side_pcd, side2_pcd, back_pcd, front_pcd, axis_aligned_bounding_box])


# combined_pcd = o3d.geometry.PointCloud()
# combined_pcd += side_pcd
# combined_pcd += side2_pcd
# combined_pcd += back_pcd
# combined_pcd += front_pcd
# o3d.io.write_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\combined_filtered_toy_car.ply", combined_pcd)








# MISC ---------------------------------------

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
