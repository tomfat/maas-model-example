import os
from label_studio_ml.model import LabelStudioMLBase


# TODO: remove work around code
#       Label Studio Bug：Relations的标注Tag不能被正常解析
import label_studio.core.label_config
label_studio.core.label_config._LABEL_TAGS.add('Relation')


class ModelEntry(LabelStudioMLBase):
    def __init__(self, **kwargs):
        super(ModelEntry, self).__init__(**kwargs)

        # 从self.parsed_label_config中读取label信息, 参考样例：
        """
        {
            'relations': {
                'type': 'Relations',
                'to_name': ['text'],
                'labels': ['relation:董事', 'attribute:创建时间'],
            },
            'entities': {
                'type': 'Labels',
                'to_name': ['text'],
                'labels': ['entity:公司', 'entity:人名', 'entity:时间'],
            }
        }
        """
        self.from_name = 'entities'
        self.to_name = self.parsed_label_config[self.from_name]['to_name'][0]
        self.label_list = self.parsed_label_config[self.from_name]['labels']

        # 根据self.train_output决定是否load已经训练好的模型
        if self.train_output is None or len(self.train_output) == 0:
            self._init_model()
        else:
            self._load_model()

    def _init_model(self):
        pass

    def _load_model(self):
        print(f"train_output = {self.train_output}")

    def fit(self, tasks, workdir=None, lr=0.1, batch_size=8, num_epoch=20, **kwargs):
        """
        :param tasks: 训练数据集，格式参考test/test_model.py中的ENTITY_RELATION_ANNO
        :param workdir: 工作目录，保存权重等需要被持久化的数据
        :param kwargs: 超参，可以自定义，例如：lr=0.1, batch_size=8, num_epoch=20
        :return: train_output: dict
        """

        # 训练模型，并将权重等保存在workdir中

        with open(os.path.join(workdir, 'weights.txt'), 'w') as output_file:
            output_file.write('NOTHING')

        return {
            "model_weights": os.path.join(workdir, 'weights.txt'),
            # 这里返回的dict，在下次模型被初始化的时候会作为self.train_output传入
        }

    def predict(self, tasks, **kwargs):
        """
        :param tasks: 待预测的数据，格式参考test/test_model.py中的ENTITY_RELATION_ANNO
        :param kwargs:
        :return: 预测结果，格式参考test/test_model.py中的ENTITY_RELATION_ANNO
        """

        predictions = []

        # 模型预测
        for task in tasks:
            text = task['data']['text']
            # 伪代码, 随机生成一个实体
            import random
            start = random.randint(0, len(text))
            end = random.randint(start, len(text))
            label = self.label_list[random.randint(0, len(self.label_list) - 1)]

            predictions.append({
                'result': [{
                    "value": {
                        "start": start,
                        "end": end,
                        "text": text[start:end],
                        "labels": [label],
                        "from_name": self.from_name,
                        "to_name": self.to_name
                    },
                    "score": 1.0
                }],

            })
        return predictions
