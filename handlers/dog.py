from tornado.web import RequestHandler
from keras.preprocessing import image
from keras.layers import GlobalAveragePooling2D
from keras.layers import Dropout, Dense
from keras.models import Sequential
from glob import glob
import numpy as np
from io import BytesIO
from keras.applications.xception import Xception, preprocess_input

# 从另一个预训练的CNN获取bottleneck特征
BOTTLENECK_SHAPE = (7, 7, 2048)

Xception_model = Sequential()
Xception_model.add(GlobalAveragePooling2D(input_shape=BOTTLENECK_SHAPE))
Xception_model.add(Dropout(0.21))
Xception_model.add(Dense(133, activation='softmax'))
# 编译模型
Xception_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# 加载具有最佳验证loss的模型权重
Xception_model.load_weights('weights/weights.best.Xception.hdf5')

# load list of dog names
dog_names = [item[20:-1] for item in sorted(glob("/data/dog_images/train/*/"))]

ex = Xception(weights='imagenet', include_top=False)


def path_to_tensor(img_path):
    # 用PIL加载RGB图像为PIL.Image.Image类型
    img = image.load_img(img_path, target_size=(224, 224))
    # 将PIL.Image.Image类型转化为格式为(224, 224, 3)的3维张量
    x = image.img_to_array(img)
    # 将3维张量转化为格式为(1, 224, 224, 3)的4维张量并返回
    return np.expand_dims(x, axis=0)


# 该函数将图像的路径作为输入
# 然后返回此模型所预测的狗的品种
def Xception_predict_breed(img_path):
    bottleneck_feature = ex.predict(preprocess_input(path_to_tensor(img_path)))
    predicted_vector = Xception_model.predict(bottleneck_feature)
    return dog_names[np.argmax(predicted_vector)]


class JudgeDogHandler(RequestHandler):
    def post(self, *args, **kwargs):
        file_imgs = self.request.files.get('newImg', None)  # 获取上传文件数据，返回文件列表
        if len(file_imgs) <= 0:
            self.set_status(400, 'bad request')
            return
        file_img = file_imgs[0]
        try:
            self.write(Xception_predict_breed(BytesIO(file_img['body'])))
        except:
            self.set_status(400, 'bad request')

