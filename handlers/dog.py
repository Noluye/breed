from tornado.web import RequestHandler
from keras.preprocessing import image
from keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.layers import Dropout, Flatten, Dense
from keras.models import Sequential
from glob import glob
import numpy as np
from PIL import Image

# 从另一个预训练的CNN获取bottleneck特征
bottleneck_features = np.load('/data/bottleneck_features/DogXceptionData.npz')
train_Xception = bottleneck_features['train']
valid_Xception = bottleneck_features['valid']
test_Xception = bottleneck_features['test']


def extract_Xception(tensor):
    from keras.applications.xception import Xception, preprocess_input
    return Xception(weights='imagenet', include_top=False).predict(preprocess_input(tensor))


def path_to_tensor(img_path):
    # 用PIL加载RGB图像为PIL.Image.Image类型
    img = image.load_img(img_path, target_size=(224, 224))
    # 将PIL.Image.Image类型转化为格式为(224, 224, 3)的3维张量
    x = image.img_to_array(img)
    # 将3维张量转化为格式为(1, 224, 224, 3)的4维张量并返回
    return np.expand_dims(x, axis=0)


# def raw_image_to_tensor(raw_image):
#     img = Image.open(raw_image)
#     target = (224, 224)
#     img = img.resize(target)
#     img = image.img_to_array(img)
#     return img
Xception_model = Sequential()
Xception_model.add(GlobalAveragePooling2D(input_shape=train_Xception.shape[1:]))
Xception_model.add(Dropout(0.21))
Xception_model.add(Dense(133, activation='softmax'))
print(Xception_model.summary())

# 编译模型
Xception_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 加载具有最佳验证loss的模型权重
Xception_model.load_weights('weights/weights.best.Xception.hdf5')

# load list of dog names
dog_names = [item[20:-1] for item in sorted(glob("/data/dog_images/train/*/"))]


# 该函数将图像的路径作为输入
# 然后返回此模型所预测的狗的品种
def Xception_predict_breed(img_path):
    bottleneck_feature = extract_Xception(path_to_tensor(img_path))
    predicted_vector = Xception_model.predict(bottleneck_feature)
    return dog_names[np.argmax(predicted_vector)]


class JudgeDogHandler(RequestHandler):
    def post(self, *args, **kwargs):
        file_imgs = self.request.files.get('newImg', None)  # 获取上传文件数据，返回文件列表
        if len(file_imgs) <= 0:
            self.set_status(400, 'bad request')
            return
            # filename 文件的实际名字，body 文件的数据实体；content_type 文件的类型。 这三个对象属性可以像字典一样支持关键字索引
        file_img = file_imgs[0]
        save_to = 'uploads/{}'.format(file_img['filename'])
        print(save_to)
        # 以二进制格式打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。一般用于非文本文件如图片等。
        with open(save_to, 'wb') as f:  # 二进制
            f.write(file_img['body'])
        # 用PIL加载RGB图像为PIL.Image.Image类型
        # raw_image_to_tensor("uploads/bomei1.jpg")
        # path_to_tensor("uploads/bomei1.jpg")
        self.write(Xception_predict_breed(save_to))
