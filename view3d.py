import open3d as o3d
pcd = o3d.io.read_point_cloud("./output/20210729204304.ply")
vis = o3d.visualization.Visualizer()
vis.create_window()

#将点云添加至visualizer
vis.add_geometry(pcd)

#让visualizer渲染点云
vis.poll_events()
vis.update_renderer()
vis.run()

