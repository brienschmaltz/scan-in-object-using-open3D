#merge point clouds based on souce.
#http://www.open3d.org/docs/latest/tutorial/Advanced/global_registration.html


import copy
import open3d as o3d
import numpy as np

def main():
    voxel_size = 0.001 # means mm for this dataset

    #Use ICP stepwise around the manually aligned combined pcd to fill in missing details. This should complete the model. 
    #Examine results
    #start at 30 degrees and increment in 30 degrees

    print("Applying 30 degrees to combined pcd using ICP")
    target_1 = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\30 pcd.ply")
    source_1 = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\combined_filtered_toy_car.ply")
    
    o3d.visualization.draw_geometries([source_1])

    source_down_1, source_fpfh_1 = preprocess_point_cloud(source_1, voxel_size)
    target_down_1, target_fpfh_1 = preprocess_point_cloud(target_1, voxel_size)
    result_ransac_1 = execute_global_registration(source_down_1, target_down_1, source_fpfh_1, target_fpfh_1, voxel_size)
    
    #Apply transform to target (translated angle)
    #target_down_1.transform(result_ransac_1.transformation)

    #translated_target = target_down_1
    #Add translated target to combined pcd
    #source_1 += translated_target

    #o3d.visualization.draw_geometries([source_1])

    draw_registration_result(source_down_1, target_down_1, result_ransac_1.transformation)

#     #-----------------------
#     print("Applying 60 degrees to combined pcd using ICP")
#     target_2 = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\60 pcd.ply")
    
#     source_down_2, source_fpfh_2 = preprocess_point_cloud(source_1, voxel_size)
#     target_down_2, target_fpfh_2 = preprocess_point_cloud(target_2, voxel_size)
#     result_ransac_2 = execute_global_registration(source_down_2, target_down_2, source_fpfh_2, target_fpfh_2, voxel_size)
    
#     #Apply transform to target (translated angle)
#     target_down_2.transform(result_ransac_2.transformation)

#     translated_target_2 = target_down_2
#     #Add translated target to combined pcd
#     source_1 += translated_target_2

#    # draw_registration_result(source_down_2, target_down_2, result_ransac_2.transformation)

#     #-----------------------
#     #I did not take a 120 degree angle that is why it is skipped 
#     print("Applying 150 degrees to combined pcd using ICP")
#     target_3 = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\150 pcd.ply")
   
    
#     source_down_3, source_fpfh_3 = preprocess_point_cloud(source_1, voxel_size)
#     target_down_3, target_fpfh_3 = preprocess_point_cloud(target_3, voxel_size)
#     result_ransac_3 = execute_global_registration(source_down_3, target_down_3, source_fpfh_3, target_fpfh_3, voxel_size)
    
#     #Apply transform to target (translated angle)
#     target_down_3.transform(result_ransac_3.transformation)

#     translated_target_3 = target_down_3
#     #Add translated target to combined pcd
#     source_1 += translated_target_3

#     #draw_registration_result(source_down_3, target_down_3, result_ransac_3.transformation)

#     #-----------------------
#     print("Applying 210 degrees to combined pcd using ICP")
#     target_4 = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\210 pcd.ply")

#     source_down_4, source_fpfh_4 = preprocess_point_cloud(source_1, voxel_size)
#     target_down_4, target_fpfh_4 = preprocess_point_cloud(target_4, voxel_size)
#     result_ransac_4 = execute_global_registration(source_down_4, target_down_4, source_fpfh_4, target_fpfh_4, voxel_size)
    
#     #Apply transform to target (translated angle)
#     target_down_4.transform(result_ransac_4.transformation)

#     translated_target_4 = target_down_4
#     #Add translated target to combined pcd (Could skip a step here)
#     source_1 += translated_target_4

#     #draw_registration_result(source_down_4, target_down_4, result_ransac_4.transformation)

#     #-----------------------
#     print("Applying 240 degrees to combined pcd using ICP")
#     target_5 = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\240 pcd.ply")
    
#     source_down_5, source_fpfh_5 = preprocess_point_cloud(source_1, voxel_size)
#     target_down_5, target_fpfh_5 = preprocess_point_cloud(target_5, voxel_size)
#     result_ransac_5 = execute_global_registration(source_down_5, target_down_5, source_fpfh_5, target_fpfh_5, voxel_size)
    
#     #Apply transform to target (translated angle)
#     target_down_5.transform(result_ransac_5.transformation)

#     translated_target_5 = target_down_5
#     #Add translated target to combined pcd
#     source_1 += translated_target_5

#     #draw_registration_result(source_down_5, target_down_5, result_ransac_5.transformation)

#     #-----------------------
#     print("Applying 300 degrees to combined pcd using ICP")
#     target_6 = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\300 pcd.ply")
    
#     source_down_6, source_fpfh_6 = preprocess_point_cloud(source_1, voxel_size)
#     target_down_6, target_fpfh_6 = preprocess_point_cloud(target_6, voxel_size)
#     result_ransac_6 = execute_global_registration(source_down_6, target_down_6, source_fpfh_6, target_fpfh_6, voxel_size)
    
#     #Apply transform to target (translated angle)
#     target_down_6.transform(result_ransac_6.transformation)

#     translated_target_6 = target_down_6
#     #Add translated target to combined pcd
#     source_1 += translated_target_6

#     #draw_registration_result(source_down_5, target_down_5, result_ransac_5.transformation)

#     #-----------------------
#     print("Applying 330 degrees to combined pcd using ICP")
#     target_7 = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\330 pcd.ply")
    
#     source_down_7, source_fpfh_7 = preprocess_point_cloud(source_1, voxel_size)
#     target_down_7, target_fpfh_7 = preprocess_point_cloud(target_7, voxel_size)
#     result_ransac_7 = execute_global_registration(source_down_7, target_down_7, source_fpfh_7, target_fpfh_7, voxel_size)
    
#      #Apply transform to target (translated angle)
#     target_down_7.transform(result_ransac_7.transformation)

#     translated_target_7 = target_down_7
#     #Add translated target to combined pcd
#     source_1 += translated_target_7
#     #draw_registration_result(source_down_5, target_down_5, result_ransac_5.transformation)

#     o3d.visualization.draw_geometries([source_1])

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    o3d.visualization.draw_geometries([source_temp, target_temp])

def preprocess_point_cloud(pcd, voxel_size):
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2
    print(":: Estimate normal with search radius %.3f." % radius_normal)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5
    print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh


def execute_global_registration(source_down, target_down, source_fpfh, target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.0
    print(":: RANSAC registration on downsampled point clouds.")
    print("   Since the downsampling voxel size is %.3f," % voxel_size)
    print("   we use a liberal distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        3, [o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(distance_threshold)], 
            o3d.pipelines.registration.RANSACConvergenceCriteria(1000000, 0.999))
    return result
#RANSACConvergenceCriteria. It defines the maximum number of RANSAC iterations and the maximum number of validation steps. 
# The larger these two numbers are, the more accurate the result is, but also the more time the algorithm takes.





if __name__ == "__main__":
    main()