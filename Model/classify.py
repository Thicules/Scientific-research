import cv2
import os
import shutil
import xml.etree.ElementTree as ET

#Lưu ý: Mỗi lần phân loại nhớ thay đường dẫn, để duyệt từng folder cho chắc (thay 7 lần)
#đường dẫn tới file images của từng folder nước 
images_dir = 'C:/Scientific-research/Road Classification/RoadImages/RDD2022/United_States/train/images' 
#đường dẫn tới file annotations của từng folder nước 
annotations_dir = 'C:/Scientific-research/Road Classification/RoadImages/RDD2022/United_States/train/annotations/xmls'

#đường dẫn tới folder phân loại đã tạo
bad_road_dir = 'C:/Scientific-research/Road Classification/train/Bad road'
good_road_dir = 'C:/Scientific-research/Road Classification/train/Good road'

for image_file in os.listdir(images_dir):
    # Đọc ảnh
    image_path = os.path.join(images_dir, image_file)
    image = cv2.imread(image_path)

    # Đọc file XML
    annotation_file = os.path.splitext(image_file)[0] + '.xml'
    annotation_path = os.path.join(annotations_dir, annotation_file)
    tree = ET.parse(annotation_path)
    
    root = tree.getroot()

    # Nếu file XML chứa nhiều hơn một object, chuyển ảnh vào thư mục Bad road
    if len(root.findall('.//object')) > 0:
        new_image_file = os.path.splitext(image_file)[0] + '.jpg'
        new_image_path = os.path.join(bad_road_dir, new_image_file)
        shutil.move(image_path, new_image_path)
    # Ngược lại, chuyển ảnh vào thư mục Good road
    else:
        new_image_file = os.path.splitext(image_file)[0] + '.jpg'
        new_image_path = os.path.join(good_road_dir, new_image_file)
        shutil.move(image_path, new_image_path)
