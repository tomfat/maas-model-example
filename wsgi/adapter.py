from label_studio_ml.model import LabelStudioMLBase


class ModelAdapter(LabelStudioMLBase):

    def __init__(self, **kwargs):
        super(ModelAdapter, self).__init__(**kwargs)
        # TODO: self.model_entry = ModelEntry()

    def predict(self, tasks, **kwargs):
        # TODO: self.model_entry.predict()
        pass

    def fit(self, tasks, workdir=None, **kwargs):
        # TODO: 增加NNI的代码
        # TODO:     从NNI获取超参组合
        # TODO:     自动划分测试集与训练集的功能

        # TODO:     self.model_entry.fit()

        # TODO:     模型评估的代码
        # TODO:     评估结果反馈给NNI
        pass


if __name__ == '__main__':
    # TODO: 分布式训练时从命令行启动训练
    pass

