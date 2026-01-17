class ProviderNotConfiguredError(RuntimeError):
    """Raised when a requested provider is missing configuration."""


class VectorStoreNotReadyError(RuntimeError):
    """Raised when the vector store is not available."""
