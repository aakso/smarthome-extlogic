import logging
import datetime
import functools
import time
import threading
import importlib
import inspect
import lib.log
from collections import OrderedDict

logger = logging.getLogger('')

class ExtLogicPlugin():
    SCHEDULE_RUN_LOGICS = 'Extended Logic run'
    LOG_BUFFER_SIZE = 100

    def __init__(self, smarthome, logic_classes=None):
        self._sh = smarthome
        self._logic_classes = []
        self._logic_items = {}

        self._parse_logics_conf(logic_classes)
        self._init_logics()

        smarthome.scheduler.add(
            self.SCHEDULE_RUN_LOGICS,
            self._run_logics,
            cycle=600,
            offset=120,
            prio=5
        )
        self._log = lib.log.Log(smarthome,
            'env.extlogic.log',
            ['time', 'name', 'level', 'message'],
            maxlen=self.LOG_BUFFER_SIZE)

    def run(self):
        self.alive = True

    def stop(self):
        self.alive = False
 
    def update_item(self, item, caller=None, source=None, dest=None):
        pass

    def parse_item(self, item):
        if 'extlogic_class' in item.conf:
            self._logic_items[item.conf['extlogic_class']] = item

    def _run_logics(self):
        for logic in self._loaded_logics:
            class_name = type(logic).__name__

            logic_item = self._logic_items.get(class_name, None)
            if not logic_item is None and logic_item() == False: 
                logger.debug("Skipping logic: {}".format(class_name))
                continue

            logger.debug("Running extended logic: {}".format(class_name))
            logic.run()

    def event_log(self, message, level='INFO', emitter=None):
        if not emitter: emitter = type(self).__name__
        stamp = self._sh.now()
        #message = '{}: {}'.format(emitter, message)
        self._log.add([stamp, emitter, level, message])
        
    def _init_logics(self):
        args = {
            'sh': self._sh,
            'plugin': self
        }
        self._loaded_logics = [a(**args) for a in self._logic_classes]
        
    def _parse_logics_conf(self, logic_classes):
        # Parse and load logic classes
        if not isinstance(logic_classes, list):
            logic_classes = [logic_classes]

        for class_location in logic_classes:
            class_path, _, class_name = class_location.partition(':')
            module = importlib.import_module(class_path)

            cls = getattr(module, class_name)
            self._logic_classes.append(cls)


class ExtLogicBase(object):
    def __init__(self, **args):
        self.sh = args.get('sh', None)
        self.plugin = args.get('plugin', None)

        self.candidate_settings = OrderedDict()
        self.candidate_settings_refs = OrderedDict()

    def set(self, k, v, **params):
        ref = params.get('ref', None)
        if not 'ref' in params.keys(): 
            ref = '{}:{}'.format(type(self).__name__, inspect.stack()[1][3])
        self.candidate_settings[k] = v
        self.candidate_settings_refs[k] = ref

    def relative_set(self, k, v, **params):
        ref = params.get('ref', None)
        if not 'ref' in params.keys():
            ref = '{}:{}'.format(type(self).__name__, inspect.stack()[1][3])
        current = self.get(k)
        self.candidate_settings[k] = current + v
        self.candidate_settings_refs[k] = ref

    def get(self, k):
        if k in self.candidate_settings.keys():
            return self.candidate_settings[k]
        else:
            return k()

    def commit(self):
        while self.candidate_settings:
            k, v = self.candidate_settings.popitem()
            if k() != v:
                ref = self.candidate_settings_refs[k]
                logger.info("Set {}: {} -> {} (ref: {})".format(k,k(),v,ref))
                self.plugin.event_log("{}#{}: {} -> {} (ref: {})"\
                    .format(type(self).__name__,k,k(),v,ref))
                k(v)

    def run(self):
        # Call user logic
        self.logic()

        # Apply changes if any
        self.commit()


