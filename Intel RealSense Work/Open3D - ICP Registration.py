#merge point clouds based on souce.
#http://www.open3d.org/docs/latest/tutorial/Advanced/global_registration.html

#Look into pyoints

import copy
import open3d as o3d
import numpy as np

def main():
    print("Gathering files...")
    voxel_size = 0.005 # means mm for this dataset
    source, target, source_down, target_down, source_fpfh, target_fpfh = prepare_dataset(voxel_size)
    result_ransac = execute_global_registration(source_down, target_down, source_fpfh, target_fpfh, voxel_size)
    
    print(result_ransac)
    draw_registration_result(source_down, result_ransac.transformation)

    #Gather other point clouds and append together for futher processing    
    front_pcd = o3d.io.read_point_cloud(r"data\Toy Truck PLY files\Filtered\Regression Filter\filtered_front_pcd_final.ply")
    back_pcd = o3d.io.read_point_cloud(r"data\Toy Truck PLY files\Filtered\Regression Filter\filtered_back_pcd.ply")
    side_pcd= o3d.io.read_point_cloud(r"data\Toy Truck PLY files\Filtered\Regression Filter\filtered_side_pcd.ply")
    side2_pcd = o3d.io.read_point_cloud(r"data\Toy Truck PLY files\Filtered\Regression Filter\filtered_side2_pcd.ply")
    top_pcd = o3d.io.read_point_cloud(r"data\Toy Truck PLY files\top_view.ply") 
    
    combined_pcd = source_down
    combined_pcd += target_down
    o3d.visualization.draw_geometries([combined_pcd])

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
    print(":: Load two point clouds and disturb initial pose.")
    source = o3d.io.read_point_cloud(r"data\Toy Truck PLY files\Filtered\Regression Filter\filtered_side_pcd.ply")
    target = o3d.io.read_point_cloud(r"data\Toy Truck PLY files\150 degree.ply")
    draw_registration_result(source, target, np.identity(4))

    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)
    return source, target, source_down, target_down, source_fpfh, target_fpfh

def execute_global_registration(source_down, target_down, source_fpfh, target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    print(":: RANSAC registration on downsampled point clouds.")
    print("   Since the downsampling voxel size is %.3f," % voxel_size)
    print("   we use a liberal distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        3, [o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(distance_threshold)], 
            o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999))
    return result
#RANSACConvergenceCriteria. It defines the maximum number of RANSAC iterations and the maximum number of validation steps. 
# The larger these two numbers are, the more accurate the result is, but also the more time the algorithm takes.





if __name__ == "__main__":
    main()