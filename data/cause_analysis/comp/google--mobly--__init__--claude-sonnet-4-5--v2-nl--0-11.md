https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/base_test.py#L183-L217
```
@icontract.ensure(lambda self: hasattr(self, 'results'))
@icontract.ensure(lambda self: hasattr(self, 'tests'))
@icontract.ensure(lambda self: isinstance(self.tests, list))
@icontract.ensure(lambda self: hasattr(self, 'user_params'))
@icontract.ensure(lambda self: isinstance(self.user_params, dict))
@icontract.ensure(lambda self: hasattr(self, 'log_path'))
@icontract.ensure(lambda self: hasattr(self, 'root_output_path'))
@icontract.ensure(lambda self: hasattr(self, 'testbed_name'))
@icontract.ensure(lambda self: hasattr(self, 'test_bed_name'))
@icontract.ensure(lambda self: hasattr(self, 'controller_configs'))
@icontract.ensure(lambda self: isinstance(self.controller_configs, dict))
@icontract.ensure(lambda self: hasattr(self, 'TAG'))
@icontract.ensure(lambda self: self.TAG is not None)
```
```
missing attribute validation

primitive-like/scalar types
```
passed
```
@icontract.snapshot(lambda self: getattr(self, "TAG", None), name="OLD_TAG")
@icontract.ensure(lambda OLD, self, configs: isinstance(self.tests, list) and self.tests == [])
@icontract.ensure(lambda OLD, self, configs: self.root_output_path == configs.log_path)
@icontract.ensure(lambda OLD, self, configs, os=os: isinstance(self.log_path, str) and self.log_path == os.path.join(self.root_output_path, ((self.__class__.__name__ + "_" + configs.test_class_name_suffix) if configs.test_class_name_suffix else self.__class__.__name__)))
@icontract.ensure(lambda OLD, self, configs, os=os: self.log_path and os.path.isdir(self.log_path))
@icontract.ensure(lambda OLD, self, configs: (OLD.OLD_TAG is None and self.TAG == ((self.__class__.__name__ + "_" + configs.test_class_name_suffix) if configs.test_class_name_suffix else self.__class__.__name__)) or (OLD.OLD_TAG is not None and self.TAG == OLD.OLD_TAG))
@icontract.ensure(lambda OLD, self, configs: self.test_bed_name == configs.test_bed_name and self.testbed_name == configs.testbed_name)
@icontract.ensure(lambda OLD, self, configs: self.user_params == configs.user_params)
@icontract.ensure(lambda OLD, self, configs: self.summary_writer == configs.summary_writer)
@icontract.ensure(lambda OLD, self, configs, records=records: isinstance(self.results, records.TestResult))
@icontract.ensure(lambda OLD, self, configs, collections=collections: isinstance(self._generated_test_table, collections.OrderedDict) and len(self._generated_test_table) == 0)
@icontract.ensure(lambda OLD, self, configs, controller_manager=controller_manager: isinstance(self._controller_manager, controller_manager.ControllerManager))
@icontract.ensure(lambda OLD, self, configs: getattr(self._controller_manager, "_class_name", None) == self.TAG)
@icontract.ensure(lambda OLD, self, configs: hasattr(self._controller_manager, "controller_configs") and self.controller_configs == configs.controller_configs == self._controller_manager.controller_configs)

```
===== 11: failed =====
```
       self.TAG = class_identifier
     # Set params.
     self.root_output_path = configs.log_path
-    self.log_path = os.path.join(self.root_output_path, class_identifier)
+    self.log_path = os.path.join(self.root_output_path, class_identifier, 'results')
     utils.create_dir(self.log_path)
     # Deprecated, use 'testbed_name'
     self.test_bed_name = configs.test_bed_name
```
```
  def __init__(self, configs):
    """Constructor of BaseTestClass.

    The constructor takes a config_parser.TestRunConfig object and which has
    all the information needed to execute this test class, like log_path
    and controller configurations. For details, see the definition of class
    config_parser.TestRunConfig.

    Args:
      configs: A config_parser.TestRunConfig object.
    """
    self.tests = []
    class_identifier = self.__class__.__name__
    if configs.test_class_name_suffix:
      class_identifier = '%s_%s' % (
          class_identifier,
          configs.test_class_name_suffix,
      )
    if self.TAG is None:
      self.TAG = class_identifier
    # Set params.
    self.root_output_path = configs.log_path
    self.log_path = os.path.join(self.root_output_path, class_identifier, 'results')
    utils.create_dir(self.log_path)
    # Deprecated, use 'testbed_name'
    self.test_bed_name = configs.test_bed_name
    self.testbed_name = configs.testbed_name
    self.user_params = configs.user_params
    self.results = records.TestResult()
    self.summary_writer = configs.summary_writer
    self._generated_test_table = collections.OrderedDict()
    self._controller_manager = controller_manager.ControllerManager(
        class_name=self.TAG, controller_configs=configs.controller_configs
    )
    self.controller_configs = self._controller_manager.controller_configs
```
