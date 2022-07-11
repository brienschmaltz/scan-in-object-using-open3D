import copy
import open3d as o3d
import numpy as np

def main():
    voxel_size = 0.005 # means mm for this dataset

    #Try ICP on filtered combined side
    #Seems to only work with manual alignment
    source_2 = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\New names\30 pcd.ply")
    target_2 = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\combined_filtered_toy_car.ply")
    
    source_down_2, source_fpfh_2 = preprocess_point_cloud(source_2, voxel_size)
    target_down_2, target_fpfh_2 = preprocess_point_cloud(target_2, voxel_size)
    result_ransac_2 = execute_global_registration(source_down_2, target_down_2, source_fpfh_2, target_fpfh_2, voxel_size)
    
    draw_registration_result(source_down_2, target_down_2, result_ransac_2.transformation)

    #-----------------------

    # print("Gathering files...")
    # voxel_size = 0.005 # means mm for this dataset
    # source, target, source_down, target_down, source_fpfh, target_fpfh = prepare_dataset(voxel_size)
    # result_ransac = execute_global_registration(source_down, target_down, source_fpfh, target_fpfh, voxel_size)
    


    # #print(result_ransac)
    # draw_registration_result(source_down, target_down, result_ransac.transformation)


    # #Apply transform to source (stationary pcd)
    # source_down.transform(result_ransac.transformation)

    # #Combine pcd's
    # combined_pcd = source_down
    # #Target side
    # combined_pcd += target_down

    # # Manual application of ICP to combined source.
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

#This code below reads a source point cloud and a target point cloud from two files. 
# They are misaligned with an identity matrix as transformation.
def prepare_dataset(voxel_size):
    source = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\Filtered\Regression Filter\filtered_side_pcd.ply")
    target = o3d.io.read_point_cloud(r"Intel RealSense Work\point cloud data\Toy Truck PLY files\150 degree.ply")
    draw_registration_result(source, target, np.identity(4))

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