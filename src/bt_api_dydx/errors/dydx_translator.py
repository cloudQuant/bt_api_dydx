from bt_api_base.error import ErrorTranslator


class DydxErrorTranslator(ErrorTranslator):
    """dYdX error translator - delegates to base for dict responses."""

    @classmethod
    def translate(cls, raw_error: dict, venue: str):
        """Translate dYdX error response to UnifiedError."""
        if isinstance(raw_error, dict) and raw_error.get("code"):
            return super().translate(raw_error, venue)
        return None
