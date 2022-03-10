from enum import Enum

class ResourceCredentials:
    def __init__(self,
                 username: str,
                 password: str,
                 ca_cert: str,
                 client_cert: str,
                 client_cert_key: str,
                 ssl: bool):
        self.username = username
        self.password = password
        self.ca_cert = ca_cert
        self.client_cert = client_cert
        self.client_cert_key = client_cert_key
        self.ssl = ssl

    def reprJSON(self):
        return dict(
            username=self.username,
            password=self.password,
            ca_cert=self.ca_cert,
            client_cert=self.client_cert,
            client_cert_key=self.client_cert_key,
            ssl=self.ssl)


class EnvironmentIdentifier:
    def __init__(self, name=None, uuid=None):
        self.name = name
        self.uuid = uuid

    def reprJSON(self):
        return dict(
            name=self.name) if self.name is not None else dict(
            uuid=self.uuid)


class ResourceMetadata:
    def __init__(self, metadata: dict):
        self.metadata = metadata

    def reprJSON(self):
        return self.metadata


class ResourceType(Enum):
    POSTGRES = "postgres"
    MYSQL = "mysql"
    URL = "url"
    S3 = "s3"
    MONGODB = "mongodb"
    ELASTICSEARCH = "elasticsearch"
    SNOWFLAKE = "snowflake"
    BIGQUERY = "bigquery"
    SQLSERVER = "sqlserver"
    COSMODB = "cosmodb"


class ResourceSSHTunnel:
    def __init__(self, address: str, privateKey: str):
        self.address = address
        self.privateKey = privateKey

    def reprJSON(self):
        return dict(address=self.address, private_key=self.privateKey)


class ResourceParams:
    def __init__(self,
                 name: str,
                 url: str,
                 createCredentials: ResourceCredentials,
                 environment: EnvironmentIdentifier,
                 metadata: ResourceMetadata,
                 type: ResourceType,
                 sshTunnel: ResourceSSHTunnel):
        self.name = name
        self.url = url
        self.credentials = createCredentials
        self.environment = environment
        self.metadata = metadata
        self.type = type
        self.sshTunnel = sshTunnel

    def reprJSON(self):
        return dict(
            name=self.name,
            url=self.url,
            credentials=self.credentials,
            environment=self.environment,
            metadata=self.metadata,
            type=self.type.value,
            ssh_tunnel=self.sshTunnel
        )


class CreateResourceParams(ResourceParams):
    def __init__(
            self,
            name: str,
            url: str,
            createCredentials: ResourceCredentials,
            environment: EnvironmentIdentifier,
            metadata: ResourceMetadata,
            type: ResourceType,
            sshTunnel: ResourceSSHTunnel):
        super().__init__(
            name,
            url,
            createCredentials,
            environment,
            metadata,
            type,
            sshTunnel)


class UpdateResourceParams(ResourceParams):
    def __init__(
            self,
            name: str,
            url: str,
            createCredentials: ResourceCredentials,
            environment: EnvironmentIdentifier,
            metadata: ResourceMetadata,
            type: ResourceType,
            sshTunnel: ResourceSSHTunnel):
        super().__init__(
            name,
            url,
            createCredentials,
            environment,
            metadata,
            type,
            sshTunnel)


class ConnectorType(Enum):
    SOURCE = "source"
    DESTINATION = "Destination"


class ConnectorParams:
    def __init__(self,
                 metadata: dict[str: ConnectorType],
                 config: dict[str, str],
                 name: str,
                 resourceId: int,
                 pipelineId="",
                 pipelineName="") -> None:
        self._metadata = metadata
        self._config = config
        self._name = name
        self._resourceId = resourceId
        self._pipelineId = pipelineId
        self._pipelineName = pipelineName

    def reprJSON(self):
        return dict(
            metadata=self._metadata,
            config=self._config,
            name=self._name,
            resource_id=self._resourceId,
            pipeline_id=self._pipelineId,
            pipeline_name=self._pipelineName
        )


class CreateConnectorParams(ConnectorParams):
    def __init__(self,
                 metadata: dict[str: ConnectorType],
                 config: dict[str: str],
                 name: str,
                 resourceId: int,
                 pipelineId="",
                 pipelineName="") -> None:
        super().__init__(metadata, config, name, resourceId, pipelineId, pipelineName)


class UpdateConnectorParams(ConnectorParams):
    def __init__(self,
                 metadata: dict[str: ConnectorType],
                 config: dict[str: str],
                 name: str,
                 resourceId: int,
                 pipelineId="",
                 pipelineName="") -> None:
        super().__init__(metadata, config, name, resourceId, pipelineId, pipelineName)


class PipelineParams:
    def __init__(
            self,
            metadata: list[str],
            name: str,
            environment: EnvironmentIdentifier) -> None:
        self._metadata = metadata
        self._name = name
        self._environment = environment

    def reprJSON(self):
        return dict(
            metadata=self._metadata,
            name=self._name,
            environment=self._environment
        )


class CreatePipelineParams(PipelineParams):
    def __init__(
            self,
            metadata: list[str],
            name: str,
            environment: EnvironmentIdentifier) -> None:
        super().__init__(metadata, name, environment)


class UpdatePipelineParams(PipelineParams):
    def __init__(
            self,
            metadata: list[str],
            name: str,
            environment: EnvironmentIdentifier) -> None:
        super().__init__(metadata, name, environment)


class PipelineIdentifiers:
    def __init__(self, name) -> None:
        self._name = name

    def reprJSON(self):
        return dict(name=self._name)


class FunctionParams:
    def __init__(
            self,
            inputStream: str,
            image: str,
            command: list[str],
            args: list[str],
            pipelineIdentifiers: PipelineIdentifiers,
            envVars: dict[str, str]) -> None:
        self._inputStream = inputStream
        self._image = image
        self._command = command
        self._args = args
        self._pipeline = pipelineIdentifiers
        self._envVars = envVars

    def reprJSON(self):
        return dict(
            input_stream=self._inputStream,
            image=self._image,
            command=self._command,
            args=self._args,
            pipeline=self._pipeline,
            env_vars=self._envVars
        )


class CreateFunctionParams(FunctionParams):
    def __init__(self,
                 inputStream: str,
                 image: str,
                 command: list[str],
                 args: list[str],
                 pipelineIdentifiers: PipelineIdentifiers,
                 envVars: dict[str,
                               str]) -> None:
        super().__init__(inputStream, image, command, args, pipelineIdentifiers, envVars)


class UpdateFunctionParams(FunctionParams):
    def __init__(self,
                 inputStream: str,
                 image: str,
                 command: list[str],
                 args: list[str],
                 pipelineIdentifiers: PipelineIdentifiers,
                 envVars: dict[str,
                               str]) -> None:
        super().__init__(inputStream, image, command, args, pipelineIdentifiers, envVars)
