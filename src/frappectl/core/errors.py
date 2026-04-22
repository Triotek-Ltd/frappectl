class FrappeCtlError(Exception):
    pass


class BenchNotFoundError(FrappeCtlError):
    pass


class NoActiveBenchError(FrappeCtlError):
    pass


class ConfigError(FrappeCtlError):
    pass


class PrivilegeError(FrappeCtlError):
    pass


class UnsupportedPlatformError(FrappeCtlError):
    pass
