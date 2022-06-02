import open3d as o3d
import numpy as np

front_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\filtered_front_pcd_final.ply")
back_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\filtered_back_pcd.ply")
side_pcd= o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\filtered_side_pcd.ply")
side2_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\filtered_side2_pcd.ply")
top_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\top_view.ply") 

o3d.visualization.draw_geometries(
         [side_pcd, side2_pcd, back_pcd, front_pcd])

#make new array of the xyz cords of each point cloud
side_pcd_as_array= np.asarray(side_pcd.points)
side_pcd_as_color_array= np.asarray(side_pcd.colors)
side2_pcd_as_array= np.asarray(side2_pcd.points)
back_pcd_as_array= np.asarray(back_pcd.points)


#90 ply rotation (back side)
matrix_transform = back_pcd.get_rotation_matrix_from_xyz((0 ,0.5* np.pi,0))
back_pcd = back_pcd.rotate(matrix_transform, center=(side_pcd_as_array[:,0].mean(),side_pcd_as_array[:,1].mean(),side_pcd_as_array[:,2].mean()))
back_pcd = back_pcd.translate((-0.005,-0.03,-0.030))

#180 ply rotation (front side)
matrix_transform_1 = front_pcd.get_rotation_matrix_from_xyz((0 ,-0.5* np.pi,0))
front_pcd = front_pcd.rotate(matrix_transform_1, center=(side_pcd_as_array[:,0].mean(),side_pcd_as_array[:,1].mean(),side_pcd_as_array[:,2].mean()))
front_pcd = front_pcd.translate((-0.055,-0.02,-0.001))

#270 ply rotation (left side)
matrix_transform_2 = side2_pcd.get_rotation_matrix_from_xyz((0 ,1* np.pi,0))
side2_pcd = side2_pcd.rotate(matrix_transform_2, center=(side_pcd_as_array[:,0].mean(),side_pcd_as_array[:,1].mean(),side_pcd_as_array[:,2].mean()))
side2_pcd = side2_pcd.translate((-0.015,-0.02,0.004))

#top rotation
matrix_transform_3 = side2_pcd.get_rotation_matrix_from_xyz((-0.6* np.pi ,0,0))
top_pcd = top_pcd.rotate(matrix_transform_3, center=(side_pcd_as_array[:,0].mean(),side_pcd_as_array[:,1].mean(),side_pcd_as_array[:,2].mean()))
top_pcd = top_pcd.translate((0.01,0.12,0.1))

#Bounding box and final display
axis_aligned_bounding_box = side_pcd.get_axis_aligned_bounding_box()
axis_aligned_bounding_box.color = (1, 0, 0)
oriented_bounding_box = side_pcd.get_oriented_bounding_box()
oriented_bounding_box.color = (0, 1, 0)
print("Displaying axis_aligned_bounding_box in red and oriented bounding box in green ...")
o3d.visualization.draw_geometries(
         [side_pcd, side2_pcd, back_pcd, front_pcd, axis_aligned_bounding_box])


combined_pcd = o3d.geometry.PointCloud()
combined_pcd += side_pcd
combined_pcd += side2_pcd
combined_pcd += back_pcd
combined_pcd += front_pcd
o3d.io.write_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\combined_filtered_toy_car.ply", combined_pcd)








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
