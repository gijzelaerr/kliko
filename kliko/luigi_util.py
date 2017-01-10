import luigi
import docker
from kliko.core import kliko_runner
from abc import ABCMeta, abstractmethod
import yaml
from kliko.docker_util import extract_params
from kliko.validate import validate_kliko
import os
from kliko.chaining import _dict2sha256, _mkdir_if_not_exists
from repoze.lru import lru_cache


class FileParameter(luigi.Parameter):
    """
    Parameter whose value is a ``path``.
    """

    def parse(self, s):
        path = str(s)
        if os.path.exists(path):
            return path
        else:
            raise ValueError("Invalid file - {} does not exists!".format(path))


field_mapping = {
    'str': luigi.Parameter,
    'float': luigi.FloatParameter,
    'int': luigi.IntParameter,
    'choice': luigi.ChoiceParameter,
    'bool': luigi.BoolParameter,
    'file': FileParameter,
}


class Optional(str):
    """
    A optional Luigiparameter.
    """
    def __repr__(self):
        return "<optional>"
    __str__ = __repr__

optional = Optional()


class KlikoTask(luigi.Task):
    """
    A Luigi task that defines a Kliko task. Override the ``image_name`` method
    to specify which kliko container to run.
    """
    __metaclass__ = ABCMeta
    connection = None

    @classmethod
    def get_params(cls):
        """
        We override this so we can populate the param list with the Kliko configuration.
        """
        params = []
        if cls.image_name():
            cls.kliko_data = cls.get_kliko_data()
            for section in cls.kliko_data['sections']:
                for field in section['fields']:
                    args = {}
                    if not field.get('required', False):
                        # if not required set default value to optional, we will filter this out later
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

    @lru_cache(10)
    def get_instance_path(self):
        """
        Each Kliko image and set of paramaters has its own private folder.
        """
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
        """
        We create a .finished file to mark a task finished in a Kliko work/output folder. In the case of joined IO
        the output folder is the same as the input folder. We add the kliko container ID to the finished file to
        not confuse luigi. Don't forget to get the parent folder of the path returned by this output function.
        """
        klikodata = self.get_kliko_data()
        if klikodata['io'] == 'split':
            return luigi.LocalTarget(self.get_instance_path() + '/output/.finished')
        else:
            return luigi.LocalTarget(os.path.dirname(self.input().path) + '/.finished-{}'.format(self.image_id()[:12]))

    @classmethod
    @abstractmethod
    def image_name(cls):
        """
        override this and return the kliko container name you want to use as a string .
        """
        pass

    @classmethod
    @lru_cache(10)
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
    @lru_cache(10)
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
            work = os.path.dirname(input_.path)
            if self.get_kliko_data()['io'] == 'split':
                paths['input'] = work
            else:
                paths['work'] = work

        kliko_runner(kliko_data=self.kliko_data,
                     parameters=self.param_kwargs,
                     docker_client=docker_client,
                     image_name=self.image_name(),
                     paths=paths,
                     )

        open(self.output().path, 'a').close()
