import unittest
from pprint import pprint
from unittest.mock import patch, MagicMock

from app import CustomProxy


class TestCustomProxy(unittest.TestCase):
    def setUp(self):
        self.config_file = 'test_config.yml'
        self.custom_proxy = CustomProxy(config_file=self.config_file)
        pprint(self.custom_proxy.config)

    def test_load_handlers(self):
        with patch.object(self.custom_proxy, 'load_handler') as mock_load_handler:
            self.custom_proxy.config['handlers'] = {'/path1': 'module1.function1', '/path2': 'module2.function2'}
            handlers = self.custom_proxy.load_handlers()

            mock_load_handler.assert_called_with('module1.function1')
            mock_load_handler.assert_called_with('module2.function2')

            expected_handlers = {'/path1': mock_load_handler.return_value, '/path2': mock_load_handler.return_value}
            self.assertEqual(handlers, expected_handlers)

    def test_load_handler(self):
        with patch('builtins.__import__') as mock_import:
            mock_module = MagicMock()
            mock_function = MagicMock()
            mock_import.return_value = mock_module
            mock_module.function_name = mock_function

            handler = self.custom_proxy.load_handler('module_name.function_name')

            mock_import.assert_called_once_with('module_name', fromlist=['function_name'])
            self.assertEqual(handler, mock_function)

    @patch.object(CustomProxy, 'handlers', {'/path1': MagicMock()})
    @patch.object(CustomProxy, 'drop_paths', ['/path2'])
    def test_response(self, mock_handlers):
        flow = MagicMock()
        flow.request.path = '/path1'

        self.custom_proxy.response(flow)
        mock_handlers['/path1'].assert_called_once_with({})

        flow.request.path = '/path2'
        with patch.object(CustomProxy, 'logging') as mock_logging:
            self.custom_proxy.response(flow)
            mock_logging.info.assert_called_once_with(f"Dropping request to {flow.request.path}")

        flow.request.path = '/path3'
        self.custom_proxy.response(flow)
        mock_handlers.get.assert_not_called()


if __name__ == '__main__':
    unittest.main()
