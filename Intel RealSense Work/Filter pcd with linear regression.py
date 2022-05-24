import open3d as o3d
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def main():
    
    front_pcd = o3d.io.read_point_cloud(r"data\Toy Truck PLY files\360 degree.ply")
    back_pcd = o3d.io.read_point_cloud(r"data\Toy Truck PLY files\180 degree.ply")
    side_pcd= o3d.io.read_point_cloud(r"data\Toy Truck PLY files\90 degree.ply")
    side2_pcd = o3d.io.read_point_cloud(r"data\Toy Truck PLY files\270 degree.ply")
    top_pcd = o3d.io.read_point_cloud(r"data\Toy Truck PLY files\top_view.ply") 

    #For resusability sake
    point_cloud = back_pcd

    #make new array of the xyz cords of each point cloud
    side_pcd_as_array= np.asarray(point_cloud.points)
    side_pcd_as_color_array= np.asarray(point_cloud.colors)
    #colors = np.asarray(back_pcd.colors)
    #print(colors[0])

    print("Filter point cloud with regression line.")
    print('Before Regression Filter')
    o3d.visualization.draw(
            [point_cloud])

    #Linear Regression
    from sklearn import linear_model as lm

    # Filter the RGB color and xyz co-ordinates
    # The filter was a guess based off a histogram of the y-axis of points in side_pcd_as_array
    filter = -0.1
    filtered_side_array = side_pcd_as_array[side_pcd_as_array[:,1] < filter]

    #Make DF
    filtered_side_df = pd.DataFrame(filtered_side_array,columns=["x","y","z"])

    y_df = filtered_side_df[['y']]
    X_df = filtered_side_df[['x', 'z']]

    OLSmodel = lm.LinearRegression().fit(X_df,y_df)

    #Dr Reiman would like to mathematically find this bias. This is minor error adjustment for the regression line
    bias = 0.008

    #filtered color
    filtered_side_color_array_with_regress = side_pcd_as_color_array[side_pcd_as_array[:,1] > (OLSmodel.intercept_[0] 
                                                                    + OLSmodel.coef_[0][0] 
                                                                    * side_pcd_as_array[:,0] 
                                                                    + OLSmodel.coef_[0][1] 
                                                                    * side_pcd_as_array[:,2] + bias)]
    #filtered points
    filtered_side_array_with_regress = side_pcd_as_array[side_pcd_as_array[:,1] > (OLSmodel.intercept_[0] 
                                                                    + OLSmodel.coef_[0][0] 
                                                                    * side_pcd_as_array[:,0] 
                                                                    + OLSmodel.coef_[0][1] 
                                                                    * side_pcd_as_array[:,2] + bias)]
    #Error of regression line
    #OLSmodel_R2 = OLSmodel.score(X_df,y_df)
    #print(OLSmodel_R2)

    filtered_side_pcd = o3d.geometry.PointCloud()
    filtered_side_pcd.points = o3d.utility.Vector3dVector(filtered_side_array_with_regress)
    filtered_side_pcd.colors = o3d.utility.Vector3dVector(filtered_side_color_array_with_regress)
     
    #Display Filtered PCD 
    print('After Regression Filter')
    o3d.visualization.draw(
            [filtered_side_pcd])

    o3d.io.write_point_cloud(r"data\Toy Truck PLY files\Filtered\Regression Filter\filtered_back_pcd.ply", filtered_side_pcd)

#Finish later. Make this applicable to any PCD
def write_pcd_to_system(filtered_pcd):
    print("Writing Filtered PCD basef off regression line to system")
    #o3d.io.write_point_cloud(r"data\Toy Truck PLY files\Filtered\Regression Filter\filtered_pcd.ply", pcd)

if __name__ == "__main__":
    main()

