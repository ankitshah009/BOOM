import yaml
import json
import glog as log
from .modules import *

class Pipeline:
    "The pipeline class creates the pipeline, and manages execution."
    
    def __init__(self, conf_path):

        self._conf_path = conf_path

        with open(conf_path) as f:
        # with open('conf.yaml') as f:
            # a = yaml.load(f)
            self.conf = yaml.load(f)

        log.info('Loading configuration file from ' + conf_path)
        log.info(json.dumps(self.conf, indent=4))


        self.name = self.conf['name']
        self.n_modules = len(self.conf['modules'])

        self.modules = [eval(mod_conf['type'])(mod_conf) for mod_conf in self.conf['modules']]
        log.info('Module list: \n' + '\n\n'.join([str(x) for x in self.modules]))

        self._create_pipeline()

    def __str__(self, module=None, indent=0):
        if module == None:
            return 'Pipeline name: ' + self.name + '\n' \
                    + '  Modules:\n' \
                    + self.__str__(self.pipeline, 1)
        else:
            ans = '    | ' * (indent) + module.get_name() + '\n'
            if module.get_n_outputs() > 0:
                for child in module.get_output_modules():
                    ans += self.__str__(child, indent+1)
            return ans

    def _create_pipeline(self, module=None):
        if module == None:
            self.pipeline = self.modules[0]
            self._create_pipeline(self.pipeline)

        elif hasattr(module, 'output_files'):
            log.warn('Output module encountered')
            return module

        else:
            for tmp in self.modules:
                if not tmp in module.get_output_modules() and tmp.get_name() in module.get_conf()['output_modules']:
                    log.warn(tmp)
                    module.add_output_module(tmp)
                    tmp.add_input_module(module)
                    self._create_pipeline(tmp)

    def _check_pipeline(self, ind=0, parents=[]):
        if len(self.modules) == 0:
            return False

        self.modules[ind]
        children = self.modules[ind]

        if name not in modules:
            return False

        if "output_files" in modules[name]:
            return True

        for next_name in modules[name]['outputs']:
            if self._check_topology(next_name, modules) == False:
                return False

        return True

    def _check_types(self, name, modules):
        if "output_files" in modules[name]:
            return True

        for next_name in modules[name]['outputs']:
            if modules[name]['output_type'] != modules[next_name]['input_type']:
                return False

        for next_name in modules[name]['outputs']:
            if self._check_types(next_name, modules) == False:
                return False

        return True


    def run(self):
        self.pipeline.run()

    def draw(self, path):
        pass

