import open3d as o3d
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from varname import nameof

def main():
    
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


        #For resusability sake
        point_cloud = _330_pcd

        point_cloud2 = _240_pcd

        #make new array of the xyz cords of each point cloud
        pcd_as_array= np.asarray(point_cloud.points)
        pcd_as_color_array= np.asarray(point_cloud.colors)

        print("Filter point cloud with regression line.")
        print('Before Filter')
        o3d.visualization.draw_geometries(
                [point_cloud])

        print("-> Statistical filtering is in progress ...")
        num_neighbors = 20 # K The number of neighborhood points 
        std_ratio = 2.0 # Standard deviation multiplier 
        # Perform statistical filtering , Returns the filtered point cloud sor_pcd And the corresponding index ind
        sor_pcd, ind = point_cloud.remove_statistical_outlier(num_neighbors, std_ratio)
        sor_pcd.paint_uniform_color([0, 0, 1])
        print(" Statistical filtered point cloud ：", sor_pcd)
        sor_pcd.paint_uniform_color([0, 0, 1])
        # Extract noise point cloud 
        sor_noise_pcd = point_cloud.select_by_index(ind,invert = True)
        print(" Noise point cloud ：", sor_noise_pcd)
        sor_noise_pcd.paint_uniform_color([1, 0, 0])

        # ===========================================================
        # Visual statistical filtered point cloud and noise point cloud 
        o3d.visualization.draw_geometries([sor_pcd, sor_noise_pcd])

        #------------------ Radius filtering --------------------------
        print("-> Radius filtering in progress ...")
        num_points = 20 # The minimum number of points in the neighborhood ball , Points below this value are noise points 
        radius = 0.05 # Neighborhood radius size 
        # Perform radius filtering , Returns the filtered point cloud sor_pcd And the corresponding index ind
        sor_pcd, ind = point_cloud2.remove_radius_outlier(num_points, radius)
        sor_pcd.paint_uniform_color([0, 0, 1])
        print(" Radius filtered point cloud ：", sor_pcd)
        sor_pcd.paint_uniform_color([0, 0, 1])
        # Extract noise point cloud 
        sor_noise_pcd = point_cloud2.select_by_index(ind,invert = True)
        print(" Noise point cloud ：", sor_noise_pcd)
        sor_noise_pcd.paint_uniform_color([1, 0, 0])
        # ===========================================================
        # Visualize the point cloud and noise point cloud after radius filtering 
        o3d.visualization.draw_geometries([sor_pcd, sor_noise_pcd])

if __name__ == "__main__":
    main()

