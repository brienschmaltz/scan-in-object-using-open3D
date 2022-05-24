import open3d as o3d
import numpy as np

print("Load a 2 ply point clouds and rotate one")

front_pcd = o3d.io.read_point_cloud(r"C:\Users\Brien\Desktop\jupyterWork\MY PROJECTS\Intel RealSense\data\starbucks_cup0.ply")
side_pcd = o3d.io.read_point_cloud(r"C:\Users\Brien\Desktop\jupyterWork\MY PROJECTS\Intel RealSense\data\starbucks_cup1.ply")

#make new array of the xyz cords of each point cloud
front_pcd_as_array= np.asarray(front_pcd.points)
side_pcd_as_array= np.asarray(side_pcd.points)

colors = np.asarray(side_pcd.colors)
print(colors[0])

#print(side_pcd_as_array)
#print(side_pcd_as_array.shape)

#print(side_pcd_as_array[:,0].mean())
#print(side_pcd_as_array[:,1].mean())
#print(side_pcd_as_array[:,2].mean())
#side_pcd_as_array.transpose()

#x_change = 0.3
#with np.nditer(side_pcd_as_array, op_flags=['readwrite']) as it:
#   for x in it:
#       x[...] = x + x_change

matrix_transform = side_pcd.get_rotation_matrix_from_xyz((0 ,0.25 * np.pi,0))
side_pcd = side_pcd.rotate(matrix_transform, center=(0.05719749449452742,-0.07283343846119142,-0.2521047743007881))
side_pcd = side_pcd.translate((0.03,0,-0.03))
#Dr. Reiman and his  code
#side_pcd_as_array[:,0]+=0.3e

#Display each value in the first column of the numpy array
#for i in side_pcd_as_array[ :,1]:
    #print(i)
    #i[...] = i + x_change

# Pass numpy array to Open3D.o3d.geometry.PointCloud and visualize
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(side_pcd_as_array)
o3d.io.write_point_cloud(r"C:\Users\Brien\Desktop\jupyterWork\MY PROJECTS\Intel RealSense\data\new_starbucks_cup1.ply", pcd)

#Load in new point cloud.
new_side_pcd = o3d.io.read_point_cloud(r"C:\Users\Brien\Desktop\jupyterWork\MY PROJECTS\Intel RealSense\data\new_starbucks_cup1.ply")
front_pcd.paint_uniform_color([1, 0.706, 1])
side_pcd.paint_uniform_color([0, 0.651, 0.929])
o3d.visualization.draw_geometries([front_pcd, new_side_pcd])