import unittest
import os
from unittest.mock import patch, MagicMock

from services.agent_processors import query_engine_loader
from services.main_processors import load_vector_store
from llama_index.core import VectorStoreIndex


class TestVectorAndQueryLoader(unittest.TestCase):
    def setUp(self):
        """Set up temporary folders for testing."""
        self.empty_folder = "tests/empty_folder"
        self.non_empty_folder = "tests/non_empty_folder"

        # Create folder structure for tests
        os.makedirs(self.empty_folder, exist_ok=True)
        os.makedirs(self.non_empty_folder, exist_ok=True)

        # Create dummy files
        with open(os.path.join(self.non_empty_folder, "docstore.json"), "w") as f:
            f.write("{}")
        with open(os.path.join(self.non_empty_folder, "index_store.json"), "w") as f:
            f.write("{}")

    def tearDown(self):
        """Clean up created temporary directories."""
        import shutil
        shutil.rmtree(self.empty_folder)
        shutil.rmtree(self.non_empty_folder)

    @patch('services.main_processors.load_index_from_storage')
    @patch('services.main_processors.StorageContext')
    def test_load_vector_store_empty_folder(self, mock_storage_context, mock_load_index):
        """Test load_vector_store with an empty folder."""
        result = load_vector_store(self.empty_folder)
        self.assertIsNone(result, "load_vector_store should return None for an empty folder.")
        mock_storage_context.from_defaults.assert_not_called()
        mock_load_index.assert_not_called()

    @patch('services.main_processors.load_index_from_storage')
    @patch('services.main_processors.StorageContext')
    def test_load_vector_store_non_empty_folder(self, mock_storage_context, mock_load_index):
        """Test load_vector_store with a folder containing data."""
        # Simulate successful index loading
        mock_index = MagicMock(spec=VectorStoreIndex)
        mock_load_index.return_value = mock_index

        result = load_vector_store(self.non_empty_folder)
        self.assertIsNotNone(result, "load_vector_store should return an index for a folder with valid data.")
        mock_storage_context.from_defaults.assert_called_once_with(persist_dir=self.non_empty_folder)
        mock_load_index.assert_called_once()

    @patch('services.main_processors.load_index_from_storage')
    @patch('services.main_processors.StorageContext')
    def test_load_vector_store_failure(self, mock_storage_context, mock_load_index):
        """Test load_vector_store when an exception occurs during index loading."""
        # Simulate an exception being raised during index loading
        mock_load_index.side_effect = Exception("Loading failed.")

        result = load_vector_store(self.non_empty_folder)
        self.assertIsNone(result, "load_vector_store should return None if index loading fails due to an exception.")
        mock_storage_context.from_defaults.assert_called_once_with(persist_dir=self.non_empty_folder)
        mock_load_index.assert_called_once()

    @patch('services.agent_processors.load_vector_store')
    def test_query_engine_loader_empty_folder(self, mock_vector_loader):
        """Test query_engine_loader when vector_loader returns None for an empty folder."""
        # Simulate vector_loader returning None
        mock_vector_loader.return_value = None

        result = query_engine_loader(self.empty_folder)
        self.assertIsNone(result, "query_engine_loader should return None if load_vector_store returns None.")
        mock_vector_loader.assert_called_once_with(self.empty_folder)

    @patch('services.agent_processors.load_vector_store')
    def test_query_engine_loader_with_valid_index(self, mock_vector_loader):
        """Test query_engine_loader when vector_loader provides a valid index."""
        # Simulate valid index and query engine creation
        mock_index = MagicMock()
        mock_engine = MagicMock()
        mock_index.as_query_engine.return_value = mock_engine
        mock_vector_loader.return_value = mock_index

        result = query_engine_loader(self.non_empty_folder)
        self.assertIsNotNone(result, "query_engine_loader should return a Query Engine for a valid index.")
        self.assertEqual(result, mock_engine, "query_engine_loader should return the correct Query Engine.")
        mock_vector_loader.assert_called_once_with(self.non_empty_folder)
        mock_index.as_query_engine.assert_called_once()

    @patch('services.agent_processors.load_vector_store')
    def test_query_engine_loader_raises_exception(self, mock_vector_loader):
        """Test query_engine_loader when an exception occurs in vector_loader."""
        # Simulate an exception during vector_loader
        mock_vector_loader.side_effect = Exception("Error in vector_loader")

        with self.assertRaises(Exception,
                               msg="query_engine_loader should propagate exceptions from load_vector_store."):
            query_engine_loader(self.non_empty_folder)
        mock_vector_loader.assert_called_once_with(self.non_empty_folder)


if __name__ == '__main__':
    unittest.main()
