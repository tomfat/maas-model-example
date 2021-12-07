import random

# TODO: remove work around code
#       Label Studio Bug：Relations的标注Tag不能被正常解析
import label_studio.core.label_config
label_studio.core.label_config._LABEL_TAGS.add('Relation')

from label_studio_ml.model import LabelStudioMLBase


class ModelEntry(LabelStudioMLBase):

    def __init__(self, **kwargs):
        """
        :param label_config: 一段XML格式的标注标签，参考格式, https://labelstud.io/tags/#main。
            通常情况下不用自己Parse，通过调用基类的构造函数会自动Parse成下述格式
        XML example
        ```
        <View>
          <Relations name="rel_label" toName="text">
            <Relation value="org:founded_by"/>
            <Relation value="org:founded"/>
          </Relations>
          <Labels name="label" toName="text">
            <Label value="Organization" background="orange"/>
            <Label value="Person" background="green"/>
            <Label value="Datetime" background="blue"/>
          </Labels>
          <Text name="text" value="$text"/>
        </View>
        ```

        JSON example
        ````
        {
            "rel_label": {
                "type": "Relations",
                "to_name": [
                    "text"
                ],
                "inputs": [],
                "labels": [
                    "org:founded_by",
                    "org:founded"
                ],
                "labels_attrs": {}
            },
            "label": {
                "type": "Labels",
                "to_name": [
                    "text"
                ],
                "inputs": [{
                    "type": "Text",
                    "value": "text"
                }],
                "labels": [
                    "Organization",
                    "Person",
                    "Datetime"
                ],
                "labels_attrs": {}
            }
        }
        ```
        :param train_output: 最后一次训练的输出
        """

        super(ModelEntry, self).__init__(**kwargs)

        # pre-initialize your variables here
        _, schema = list(self.parsed_label_config.items())[0]
        self.labels = schema['labels']

        # if self.train_output is None:
        #    load_your_model
        # else:
        #    init_your_model

    def predict(self, tasks, **kwargs):
        """ This is where inference happens:
            model returns the list of predictions based on input list of tasks
            :param tasks: 待预测的内容，格式参考, https://labelstud.io/guide/export.html#Label-Studio-JSON-format-of-annotated-tasks Label Studio tasks in JSON format
        """
        results = []
        for task in tasks:
            results.append({
                'result': [{
                    'from_name': self.from_name,
                    'to_name': self.to_name,
                    'type': 'choices',
                    'value': {
                        'choices': [random.choice(self.labels)]
                    }
                }],
                'score': random.uniform(0, 1)
            })
        return results

    def fit(self, completions, workdir=None, **kwargs):
        """ This is where training happens: train your model given list of completions,
            then returns dict with created links and resources

            :param completions: 训练数据, 格式参考, https://labelstud.io/guide/export.html#Label-Studio-JSON-format-of-annotated-tasks Label Studio tasks in JSON format
            :param workdir: 当前版本的目录位置
            :param **kwargs: 其他参数，例如超参等
        """
        # save some training outputs to the job result
        # return的结果会被保存到当前workdir的job_result.json里。
        # 当下一次模型被初始化的时候，会作为train_output参数传入构造函数
        return {
            # 可以写入一些需要保留的模型配置等信息
            'random': random.randint(1, 10)
        }
