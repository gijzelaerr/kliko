import luigi
import docker
from kliko.core import kliko_runner
from abc import ABCMeta, abstractmethod
from functools import lru_cache
import yaml
from kliko.docker_util import extract_params
from kliko.validate import validate_kliko
import os
from kliko.chaining import _dict2sha256, _mkdir_if_not_exists


class FileParameter(luigi.Parameter):
    """
    Parameter whose value is a ``float``.
    """

    def parse(self, s):
        path = str(s)
        if os.path.exists(path):
            return path
        else:
            raise ValueError("Invalid file - {} does not exists!")


field_mapping = {
    'str': luigi.Parameter,
    'float': luigi.FloatParameter,
    'int': luigi.IntParameter,
    'choice': luigi.ChoiceParameter,
    'bool': luigi.BooleanParameter,
    'file': FileParameter,
}


class Optional:
    def __repr__(self):
        return "<optional>"

optional = Optional()


class KlikoTask(luigi.Task):
    __metaclass__ = ABCMeta

    connection = None

    @classmethod
    def get_params(cls):
        params = []
        if cls.imagename():
            cls.kliko_data = cls.get_kliko_data(cls.imagename())
            for section in cls.kliko_data['sections']:
                for field in section['fields']:
                    args = {}
                    if 'required' not in field:
                        args['default'] = optional
                        args['positional'] = False
                    if 'initial' in field:
                        args['default'] = field['initial']
                    if 'help_text' in field:
                        args['description'] = field['help_text']
                    if 'choices' in field:
                        args['choices'] = field['choices']
                    param = field_mapping[field['type']](**args)
                    params.append((field['name'], param))
        return params

    def output(self):
        return luigi.LocalTarget('simms/FINISHED')

    @classmethod
    @abstractmethod
    def imagename(cls):
        pass

    @classmethod
    @lru_cache()
    def image_id(cls, image_name):
        connection = cls.connect()

        img_list = connection.images(name=image_name)
        if len(img_list) == 0:
            raise Exception("image {} not found, try to build or pull it".format(image_name))
        if len(img_list) > 1:
            raise Exception("image {} matches {} images".format(image_name, len(img_list)))
        docker_image = img_list[0]
        return docker_image['Id'][7:]

    @classmethod
    @lru_cache()
    def get_kliko_data(cls, image_name):
        connection = cls.connect()
        raw_kliko_data = extract_params(connection, image_name)
        kliko_data = validate_kliko(yaml.safe_load(raw_kliko_data))
        return kliko_data

    @classmethod
    def connect(cls):
        if not cls.connection:
            cls.connection = docker.Client()
        return cls.connection

    def run(self):
        docker_client = self.connect()

        # hack to have optional arguments
        for k, v in list(self.param_kwargs.items()):
            if v == optional:
                self.param_kwargs.pop(k)

        here = os.getcwd()
        kliko_dir = os.path.join(here, ".kliko")
        id_ = self.image_id(self.imagename())
        short_id = id_[:12]

        if not os.path.isdir(kliko_dir):
            os.mkdir(kliko_dir)

        kliko_data = self.get_kliko_data(self.imagename())
        image_folder = os.path.join(kliko_dir, short_id)
        _mkdir_if_not_exists(image_folder)
        para_hash = _dict2sha256(self.param_kwargs)
        short_para_hash = para_hash[:12]
        instance_path = os.path.join(image_folder, short_para_hash)
        _mkdir_if_not_exists(instance_path)

        """
        if kliko_data['io'] == 'split':
            input_path = os.path.join(instance_path, 'input')
            _mkdir_if_not_exists(input_path)
            output_path = os.path.join(instance_path, 'output')
            _mkdir_if_not_exists(output_path)
            work_path = None
        if kliko_data['io'] == 'join':
            work_path = os.path.join(instance_path, 'work')
            _mkdir_if_not_exists(work_path)
            input_path = None
            output_path = None

        """
        kliko_runner(kliko_data=self.kliko_data,
                     parameters=self.param_kwargs,
                     docker_client=docker_client,
                     image_name=self.imagename(),
                     paths={'parent': instance_path},
                     )
