import unittest
import pytest
import json
import os
import yaml
import time
from model_entry import ModelEntry


class ModelTest(unittest.TestCase):
	def setUp(self):
		self.test_root = os.path.realpath(os.path.dirname(__file__))
		self.model_home = os.path.realpath(os.path.join(self.test_root, "../app"))
		self.model_yaml = self._load_model_yaml()
		self.train_output = None

	def _load_model_yaml(self):
		model_yaml_path = os.path.join(self.model_home, 'model.yml')
		self.assertTrue(os.path.isfile(model_yaml_path), f"未找到model.yml: {model_yaml_path}")

		try:
			with open(model_yaml_path) as inp_file:
				model_yaml = yaml.safe_load(inp_file)
		except yaml.YAMLError as e:
			self.fail(f"读取model.yml失败: {e}")

		return model_yaml

	def test_load_model_yaml(self):
		print("----测试model.yml----")
		model_yaml = self.model_yaml
		self.assertIsNotNone(model_yaml)
		self.assertIn("name", model_yaml)
		self.assertIn("type", model_yaml)
		self.assertIn(model_yaml['type'], ["Entity", "Relation"])
		self.assertIn("version", model_yaml)

		print(f"模型名称: {model_yaml['name']}")
		print(f"模型类型: {model_yaml['type']}")
		print(f"模型版本: {model_yaml['version']}")

		self.model_yaml = model_yaml

	def test_training(self):
		print("----测试模型训练----")
		input_data, label_config = self._get_training_input()
		workdir = os.path.join(self.test_root, f"maas-storage/{time.time()}")
		os.mkdir(workdir)

		os.chdir(self.model_home)

		# Init model
		model = ModelEntry(label_config=label_config, train_output=None)

		# Test training
		self.train_output = model.fit(input_data, workdir=workdir)
		print(json.dumps(self.train_output, indent=2))

		saved_files = []
		for file_name in os.listdir(workdir):
			saved_files.append(file_name)
		self.assertNotEqual(0, len(saved_files))

		print(f"Saved {len(saved_files)} files: ")
		for file_name in saved_files:
			print(f"  - {file_name}")

		with open(os.path.join(workdir, 'train_output.json'), 'w') as output_file:
			output_file.write(json.dumps(self.train_output))

	def test_prediction(self):
		print("----测试模型预测----")
		input_data, label_config = self._get_prediction_input()

		os.chdir(self.model_home)

		for dir_name in os.listdir(os.path.join(self.test_root, f"maas-storage")):
			file_path = os.path.join(self.test_root, f"maas-storage/{dir_name}/train_output.json")
			if os.path.isfile(file_path):
				with open(file_path) as train_output_file:
					self.train_output = json.loads(train_output_file.read())

		# Load model from previous training output
		model = ModelEntry(label_config=label_config, train_output=self.train_output)

		# Test prediction
		predictions = model.predict(input_data)
		self.assertIsNotNone(predictions)
		self.assertIn('result', predictions[0])
		self.assertIn('al_score', predictions[0])
		self.assertTrue(predictions[0]['al_score'] >= 0)
		self.assertTrue(predictions[0]['al_score'] <= 1)

	def _get_training_input(self):
		input_data = json.loads(ENTITY_RELATION_ANNO)
		return input_data, ENTITY_RELATION_TMPL

	def _get_prediction_input(self):
		input_data = json.loads(ENTITY_RELATION_ANNO)
		if self.model_yaml['type'] == 'Entity':
			for item in input_data:
				for anno in item['annotations']:
					anno['result'] = []
		else:  # self.model_yaml['type'] == 'Relation':
			for item in input_data:
				for anno in item['annotations']:
					anno['result'] = list(filter(lambda x: x['type'] != 'relation', anno['result']))
		return input_data, ENTITY_RELATION_TMPL


ENTITY_RELATION_TMPL = """
<View>
  <Relations name="relations" toName="text">
    <Relation value="relation:董事"/>
    <Relation value="attribute:创建时间"/>
  </Relations>
  <Labels name="entities" toName="text">
    <Label value="entity:公司" background="orange"/>
    <Label value="entity:人名" background="green"/>
    <Label value="entity:时间" background="blue"/>
  </Labels>
  <Text name="text" value="$text"/>
</View>
"""

ENTITY_RELATION_ANNO = """
[{
	"id": 3,
	"annotations": [{
		"id": 9,
		"completed_by": 1,
		"result": [{
			"value": {
				"start": 0,
				"end": 14,
				"text": "北京视野金融信息服务有限公司",
				"labels": ["entity:公司"]
			},
			"id": "8QBLN_oagf",
			"from_name": "entities",
			"to_name": "text",
			"type": "labels",
			"origin": "manual"
		}, {
			"value": {
				"start": 17,
				"end": 24,
				"text": "2015年8月",
				"labels": ["entity:时间"]
			},
			"id": "oBBWbjrTww",
			"from_name": "entities",
			"to_name": "text",
			"type": "labels",
			"origin": "manual"
		}, {
			"value": {
				"start": 26,
				"end": 28,
				"text": "程鹏",
				"labels": ["entity:人名"]
			},
			"id": "XJTNC0I68_",
			"from_name": "entities",
			"to_name": "text",
			"type": "labels",
			"origin": "manual"
		}, {
			"from_id": "8QBLN_oagf",
			"to_id": "oBBWbjrTww",
			"type": "relation",
			"direction": "right",
			"labels": ["attribute:创建时间"]
		}, {
			"from_id": "8QBLN_oagf",
			"to_id": "XJTNC0I68_",
			"type": "relation",
			"direction": "right",
			"labels": ["relation:董事"]
		}]
	}],
	"predictions": [],
	"data": {
		"text": "北京视野金融信息服务有限公司成立于2015年8月，由程鹏担任公司董事。"
	}
}]
"""