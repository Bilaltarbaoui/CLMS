import os
import tempfile
import unittest

from database.database import Database


class TestDatabasePathOverride(unittest.TestCase):
    def test_uses_env_db_path_when_set(self):
        previous = os.environ.get('CLMS_TEST_DB_PATH')
        temp_dir = tempfile.mkdtemp()
        env_path = os.path.join(temp_dir, 'clms.db')

        try:
            os.environ['CLMS_TEST_DB_PATH'] = env_path
            db = Database()
            self.assertEqual(db.database_path, env_path, 'Database should honor the CLMS_TEST_DB_PATH override.')
            self.assertTrue(os.path.exists(env_path) or os.path.exists(temp_dir))
            db.close()
        finally:
            if previous is None:
                os.environ.pop('CLMS_TEST_DB_PATH', None)
            else:
                os.environ['CLMS_TEST_DB_PATH'] = previous


if __name__ == '__main__':
    unittest.main()
