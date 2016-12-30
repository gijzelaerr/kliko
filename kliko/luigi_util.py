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
    Parameter whose value is a ``path``.
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
    """
    A Luigi task that defines a Kliko task. Override the ``image_name`` method
    to specify which kliko container to run.
    """
    __metaclass__ = ABCMeta

    connection = None

    @classmethod
    def get_param_values(cls, params, args, kwargs):
        return [(k, v) for k, v in super().get_param_values(params, args, kwargs) if v != optional]

    @classmethod
    def get_params(cls):
        params = []
        if cls.image_name():
            cls.kliko_data = cls.get_kliko_data()
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

    @lru_cache()
    def get_instance_path(self):
        here = os.getcwd()
        kliko_dir = os.path.join(here, ".kliko")
        id_ = self.image_id()
        short_id = id_[:12]

        if not os.path.isdir(kliko_dir):
            os.mkdir(kliko_dir)

        image_folder = os.path.join(kliko_dir, short_id)
        _mkdir_if_not_exists(image_folder)
        para_hash = _dict2sha256(self.param_kwargs)
        short_para_hash = para_hash[:12]

        # don't make instance path yet, do this during run
        instance_path = os.path.join(image_folder, short_para_hash)
        return instance_path

    def output(self):
        klikodata = self.get_kliko_data()
        if klikodata['io'] == 'split':
            return luigi.LocalTarget(self.get_instance_path() + '/output')
        else:
            return luigi.LocalTarget(self.get_instance_path() + '/work')

    @classmethod
    @abstractmethod
    def image_name(cls):
        pass

    @classmethod
    @lru_cache()
    def image_id(cls):
        image_name = cls.image_name()
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
    def get_kliko_data(cls):
        image_name = cls.image_name()
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

        instance_path = self.get_instance_path()
        paths = {'parent': instance_path}

        _mkdir_if_not_exists(instance_path)

        input_ = self.input()
        if input_:
            if self.get_kliko_data()['io'] == 'split':
                paths['input'] = input_.path
            else:
                paths['work'] = input_.path

        kliko_runner(kliko_data=self.kliko_data,
                     parameters=self.param_kwargs,
                     docker_client=docker_client,
                     image_name=self.image_name(),
                     paths=paths,
                     )

        finished_path = os.path.join(self.get_instance_path(), 'FINISHED')
        open(finished_path, 'a').close()
