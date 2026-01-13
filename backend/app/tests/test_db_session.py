from unittest.mock import MagicMock, patch

from app.db.session import get_db


def test_get_db_closes_session():
    with patch("app.db.session.SessionLocal") as mock_session_local:
        mock_db_instance = MagicMock()
        mock_session_local.return_value = mock_db_instance

        generator = get_db()

        db_item = next(generator)

        assert db_item == mock_db_instance

        try:
            next(generator)
        except StopIteration:
            pass

        mock_db_instance.close.assert_called_once()
