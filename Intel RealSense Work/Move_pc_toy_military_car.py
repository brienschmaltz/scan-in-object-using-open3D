import open3d as o3d
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

front_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\filtered_front_pcd_final.ply")
back_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\filtered_back_pcd.plyy")
side_pcd= o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\filtered_side_pcd.ply")
side2_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\filtered_side2_pcd.ply")
top_pcd = o3d.io.read_point_cloud(r"data\Toy Truck PLY files\top_view.ply") 

#front_pcd = o3d.io.read_point_cloud(r"data\Toy Truck PLY files\360 degree.ply")
# back_pcd = o3d.io.read_point_cloud(r"data\Toy Truck PLY files\180 degree.ply")
# side_pcd= o3d.io.read_point_cloud(r"data\Toy Truck PLY files\90 degree.ply")
# side2_pcd = o3d.io.read_point_cloud(r"data\Toy Truck PLY files\270 degree.ply")
# top_pcd = o3d.io.read_point_cloud(r"data\Toy Truck PLY files\top_view.ply") 

#make new array of the xyz cords of each point cloud
side_pcd_as_array= np.asarray(side_pcd.points)
side_pcd_as_color_array= np.asarray(side_pcd.colors)
side2_pcd_as_array= np.asarray(side2_pcd.points)

back_pcd_as_array= np.asarray(back_pcd.points)

#colors = np.asarray(back_pcd.colors)
#print(colors[0])

#Filter Point Clouds
#side_pcd_as_array[:,0]-0.1

#Not orienting ICP vs orienting it manually. 

import pandas as pd

# Filter the RGB color and xyz co-ordinates
# The filter was a guess based off a histogram of the y-axis of points in side_pcd_as_array
filter = -0.12

filtered_side_color_array = side_pcd_as_color_array[side_pcd_as_array[:,1] > filter]
filtered_side_array = side_pcd_as_array[side_pcd_as_array[:,1] > filter]

filtered_side_pcd = o3d.geometry.PointCloud()
filtered_side_pcd.points = o3d.utility.Vector3dVector(filtered_side_array)
filtered_side_pcd.colors = o3d.utility.Vector3dVector(filtered_side_color_array)
o3d.io.write_point_cloud(r"C:\Users\Brien\Desktop\jupyterWork\MY PROJECTS\Intel RealSense\data\Toy Truck PLY files\Filtered\filtered_side.ply", filtered_side_pcd)
side_filtered_pcd = o3d.io.read_point_cloud(r"C:\Users\Brien\Desktop\jupyterWork\MY PROJECTS\Intel RealSense\data\Toy Truck PLY files\Filtered\filtered_side.ply")


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
o3d.visualization.draw(
         [side_pcd, side2_pcd, back_pcd, front_pcd, axis_aligned_bounding_box])

#Combining all point clouds



# o3d.visualization.draw(
#         [oriented_bounding_box])
# #
# o3d.visualization.draw(
#         [side_pcd])

#Crop? 
vol = o3d.visualization.read_selection_polygon_volume(r"data\boundingbox.json")
crop = vol.crop_point_cloud(side_pcd)
crop.paint_uniform_color([1, 0.706, 1])
o3d.visualization.draw(
         [side_pcd, crop])

#Solution number 1 to croppping in open3d. Does not work!
# """
# corners = [[ 5.31972845 -3.21384387  0.30217625]
#  [ 5.34483288 -1.13804348  0.29917539]
#  [ 7.69983939 -1.16651864  0.30329364]
#  [ 7.67473496 -3.24231903  0.3062945 ]
#  [ 5.31845904 -3.21276837  1.03551451]
#  [ 5.34356348 -1.13696798  1.03251366]
#  [ 7.69856999 -1.16544314  1.03663191]
#  [ 7.67346556 -3.24124353  1.03963277]]
# """
# corners = np.array(...)

# # Convert the corners array to have type float64
# bounding_polygon = corners.astype("float64")

# # Create a SelectionPolygonVolume
# vol = o3d.visualization.SelectionPolygonVolume()

# # You need to specify what axis to orient the polygon to.
# # I choose the "Y" axis. I made the max value the maximum Y of
# # the polygon vertices and the min value the minimum Y of the
# # polygon vertices.
# vol.orthogonal_axis = "Y"
# vol.axis_max = np.max(bounding_polygon[:, 1])
# vol.axis_min = np.min(bounding_polygon[:, 1])

# # Set all the Y values to 0 (they aren't needed since we specified what they
# # should be using just vol.axis_max and vol.axis_min).
# bounding_polygon[:, 1] = 0

# # Convert the np.array to a Vector3dVector
# vol.bounding_polygon = o3d.utility.Vector3dVector(bounding_polygon)

# # Crop the point cloud using the Vector3dVector
# cropped_pcd = vol.crop_point_cloud(side_pcd)

# # Get a nice looking bounding box to display around the newly cropped point cloud
# # (This part is optional and just for display purposes)
# bounding_box = cropped_pcd.get_axis_aligned_bounding_box()
# bounding_box.color = (1, 0, 0)

# # Draw the newly cropped PCD and bounding box
# o3d.visualization.draw_geometries([cropped_pcd, bounding_box])


#Solution number 2 to cropping in open3d.
#Create bounding box in open3D, no documentation on this

# bounding_polygon = np.array([ 
#            [ 2.6509309513852526, 0.0, 1.6834473132326844 ],
#                                ...
#            [ 2.6579576128816544, 0.0, 1.6819127849749496 ]]).astype("float64")

# vol = o3d.visualization.SelectionPolygonVolume()

# vol.bounding_polygon = o3d.utility.Vector3dVector(bounding_polygon)

# side_pcd = vol.crop_point_cloud(vol)

#print(back_pcd_as_array)
#print(back_pcd_as_array.shape)

#print(back_pcd_as_array[:,0].mean())
#print(back_pcd_as_array[:,1].mean())
#print(back_pcd_as_array[:,2].mean())
#back_pcd_as_array.transpose()


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
