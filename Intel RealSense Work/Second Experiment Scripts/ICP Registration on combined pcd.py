import copy
import open3d as o3d
import numpy as np


# #Filtered Angles from second experiment
# _30_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second Experiment Scripts\filtered_data\_30_pcd_filtered.ply")
# _60_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second Experiment Scripts\filtered_data\_60_pcd_filtered.ply")
# _90_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second experiment Toy Truck PLY files\_90_pcd_filtered.ply")
# _120_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second experiment Toy Truck PLY files\_120_pcd_filtered.ply")
# _150_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second experiment Toy Truck PLY files\_150_pcd_filtered.ply")
# _180_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second experiment Toy Truck PLY files\_180_pcd_filtered.ply")
# _210_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second experiment Toy Truck PLY files\_210_pcd_filtered.ply")
# _240_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second experiment Toy Truck PLY files\_240_pcd_filtered.ply")
# _270_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second experiment Toy Truck PLY files\_270_pcd_filtered.ply")
# _300_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second experiment Toy Truck PLY files\_300_pcd_filtered.ply")
# _330_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second experiment Toy Truck PLY files\_330_pcd_filtered.ply")
# _360_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\Second experiment Toy Truck PLY files\_360_pcd_filtered.ply")

#Angles from first experiment
_30_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\30 pcd.ply")
_60_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\60 pcd.ply")
_90_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\90 pcd.ply")
_150_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\150 pcd.ply")
_180_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\180 pcd.ply")
_210_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\210 pcd.ply")
_240_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\240 pcd.ply")
_270_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\270 pcd.ply")
_300_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\300 pcd.ply")
_330_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\330 pcd.ply")
_360_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\360 pcd.ply")



#Filtered and Combined PCD from first experiment.
combined_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\combined_filtered_toy_car.ply")

#This is the one I will keep applying pcd's to 
final_pcd = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Final\final_toy_car.ply")


def main():

    print("Gathering files...")
    voxel_size = 0.005 # means mm for this dataset
    source, target, source_down, target_down, source_fpfh, target_fpfh = prepare_dataset(voxel_size)
    result_ransac = execute_global_registration(source_down, target_down, source_fpfh, target_fpfh, voxel_size)
    
    #print(result_ransac)
    draw_registration_result(source_down, target_down, result_ransac.transformation)


    
    # Manual application of ICP to combined source.
    # source_1 = combined_pcd
    # target_1 = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\180 degree.ply")

    # source_down_1, source_fpfh_1 = preprocess_point_cloud(source_1, voxel_size)
    # target_down_1, target_fpfh_1 = preprocess_point_cloud(target_1, voxel_size)
    # result_ransac_1 = execute_global_registration(source_down_1, target_down_1, source_fpfh_1, target_fpfh_1, voxel_size)

    # draw_registration_result(source_1, target_1, result_ransac_1.transformation)
    # source_down_1.transform(result_ransac_1.transformation)
    

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.transform(transformation)
    #o3d.visualization.draw_geometries([source_temp,target_temp])

    #Combine targets and write to system for further processing
    rolling_pcd = o3d.geometry.PointCloud()
    rolling_pcd += source_temp
    rolling_pcd += target_temp
    o3d.io.write_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Final\final_toy_car.ply", rolling_pcd)
   
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

#This code below reads a source point cloud and a target point cloud from two files. 
# They are misaligned with an identity matrix as transformation.
def prepare_dataset(voxel_size):
    #source = combined_pcd
    target = final_pcd
    source = _240_pcd
    #draw_registration_result(source, target, np.identity(4))

    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)
    return source, target, source_down, target_down, source_fpfh, target_fpfh

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
            o3d.pipelines.registration.RANSACConvergenceCriteria(4000000, 500))
    return result
#RANSACConvergenceCriteria. It defines the maximum number of RANSAC iterations and the maximum number of validation steps. 
# The larger these two numbers are, the more accurate the result is, but also the more time the algorithm takes.





if __name__ == "__main__":
    main()