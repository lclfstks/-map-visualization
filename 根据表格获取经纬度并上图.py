import pandas as pd
import requests
import folium

def geocode(api_key, address):
    base_url ="https://restapi.amap.com/v3/geocode/geo"
    params = {
        "key": api_key,
        "address": address,
        "output": "json",
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data["status"] == "1" and int(data["count"]) > 0:
            location = data["geocodes"][0]["location"].split(",")
            latitude = float(location[1])
            longitude = float(location[0])
            return latitude, longitude
        else:
            print(f"Error: {data['info']}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# 替换为您的高德地图 API key
amap_api_key = "41d76b5dca5cbbce0e01833f82d97906"

# 读取包含路口名称的 Excel 文件
input_file = "input_excel.xlsx"
df = pd.read_excel(input_file)

# 创建地图，指定中国范围
map_center = [35, 105]  # 中国中心点的经纬度
map_object = folium.Map(location=map_center, zoom_start=5)

# 创建新的 DataFrame 用于存储经纬度
columns = ["Address", "Latitude", "Longitude"]
output_df = pd.DataFrame(columns=columns)

# 循环处理每个路口名称
for index, row in df.iterrows():
    address = row.iloc[0]  # 使用 iloc[0] 获取第一列数据
    coordinates = geocode(amap_api_key, address)

    if coordinates:
        # 通过手动调整来校正坐标
        corrected_coordinates = (coordinates[0] + 0.0021, coordinates[1] - 0.0042)

        output_df = output_df.append({
            "Address": address,
            "Latitude": corrected_coordinates[0],#使用手动调整因子后的坐标纬度
            "Longitude": corrected_coordinates[1]#经度
        }, ignore_index=True)

        # 在地图上添加标记
        folium.Marker(location=corrected_coordinates, popup=address, icon=folium.Icon(color='red')).add_to(map_object)

# 保存地图为 HTML 文件
output_map_file = "output_map.html"
map_object.save(output_map_file)

# 将结果写入新的 Excel 文件
output_excel_file = "经纬度获取.xlsx"
output_df.to_excel(output_excel_file, index=False)

print(f"地理编码完成，结果保存在 {output_excel_file}，地图保存在 {output_map_file}")
