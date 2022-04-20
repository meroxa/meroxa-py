from ast import Str
from enum import Enum


class MeroxaApiResponse(object):
    def __init__(self, *args, **kwargs):
        ...


class ClientOptions:
    def __init__(self, auth: str, url: str, timeout=0.0):
        self.auth = auth
        self.timeout = timeout
        self.url = url


class ResourceCredentials:
    def __init__(
        self,
        username: str,
        password: str,
        ca_cert: str,
        client_cert: str,
        client_cert_key: str,
        ssl: bool,
    ):
        self.username = username
        self.password = password
        self.ca_cert = ca_cert
        self.client_cert = client_cert
        self.client_cert_key = client_cert_key
        self.ssl = ssl

    def repr_json(self):
        return dict(
            username=self.username,
            password=self.password,
            ca_cert=self.ca_cert,
            client_cert=self.client_cert,
            client_cert_key=self.client_cert_key,
            ssl=self.ssl,
        )


class EnvironmentIdentifier:
    def __init__(self, name=None, uuid=None):
        self.name = name
        self.uuid = uuid

    def repr_json(self):
        return dict(name=self.name) if self.name is not None else dict(uuid=self.uuid)


class ResourceMetadata:
    def __init__(self, metadata: dict):
        self.metadata = metadata

    def repr_json(self):
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

    def repr_json(self):
        return dict(address=self.address, private_key=self.privateKey)


class ResourceParams:
    def __init__(
        self,
        name: str,
        url: str,
        createCredentials: ResourceCredentials,
        environment: EnvironmentIdentifier,
        metadata: ResourceMetadata,
        type: ResourceType,
        sshTunnel: ResourceSSHTunnel,
    ):
        self.name = name
        self.url = url
        self.credentials = createCredentials
        self.environment = environment
        self.metadata = metadata
        self.type = type
        self.sshTunnel = sshTunnel

    def repr_json(self):
        return dict(
            name=self.name,
            url=self.url,
            credentials=self.credentials,
            environment=self.environment,
            metadata=self.metadata,
            type=self.type.value,
            ssh_tunnel=self.sshTunnel,
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
        sshTunnel: ResourceSSHTunnel,
    ):
        super().__init__(
            name, url, createCredentials, environment, metadata, type, sshTunnel
        )


class UpdateResourceParams(ResourceParams):
    def __init__(
        self,
        name: str,
        url: str,
        createCredentials: ResourceCredentials,
        environment: EnvironmentIdentifier,
        metadata: ResourceMetadata,
        type: ResourceType,
        sshTunnel: ResourceSSHTunnel,
    ):
        super().__init__(
            name, url, createCredentials, environment, metadata, type, sshTunnel
        )


class ConnectorType(Enum):
    SOURCE = "source"
    DESTINATION = "Destination"


class ConnectorParams:
    def __init__(
        self,
        config: dict[str, str],
        resourceName: str,
        pipelineName: str,
        metadata: dict[str, ConnectorType],
    ) -> None:
        self._config = config
        self._resourceName = resourceName
        self._pipelineName = pipelineName
        self._metadata = metadata

    def repr_json(self):
        return dict(
            config=self._config,
            resource_name=self._resourceName,
            pipeline_name=self._pipelineName,
            metadata=self._metadata,
        )


class CreateConnectorParams(ConnectorParams):
    def __init__(
        self,
        config: dict[str, str],
        resourceName: str,
        pipelineName: str,
        metadata: dict[str, ConnectorType],
    ) -> None:
        super().__init__(config, resourceName, pipelineName, metadata)


class UpdateConnectorParams(ConnectorParams):
    def __init__(
        self,
        config: dict[str, str],
        resourceName: str,
        pipelineName: str,
        metadata: dict[str, ConnectorType],
    ) -> None:
        super().__init__(config, resourceName, pipelineName, metadata)


class PipelineParams:
    def __init__(
        self, metadata: list[str], name: str, environment: EnvironmentIdentifier
    ) -> None:
        self._metadata = metadata
        self._name = name
        self._environment = environment

    def repr_json(self):
        return dict(
            metadata=self._metadata, name=self._name, environment=self._environment
        )


class CreatePipelineParams(PipelineParams):
    def __init__(
        self, metadata: list[str], name: str, environment: EnvironmentIdentifier
    ) -> None:
        super().__init__(metadata, name, environment)


class UpdatePipelineParams(PipelineParams):
    def __init__(
        self, metadata: list[str], name: str, environment: EnvironmentIdentifier
    ) -> None:
        super().__init__(metadata, name, environment)


class PipelineIdentifiers:
    def __init__(self, name) -> None:
        self._name = name

    def repr_json(self):
        return dict(name=self._name)


class FunctionParams:
    def __init__(
        self,
        uuid: str,
        name: str,
        input_stream: str,
        output_stream: str,
        image: str,
        command: list[str],
        args: list[str],
        env_vars: dict[str, str],
        pipeline: PipelineIdentifiers,
    ) -> None:
        self._uuid = uuid
        self._name = name
        self._output_stream = output_stream
        self._input_stream = input_stream
        self._image = image
        self._command = command
        self._args = args
        self._pipeline = pipeline
        self._env_vars = env_vars

    def repr_json(self):
        return dict(
            uuid=self._uuid,
            name=self._name,
            input_stream=self._input_stream,
            output_stream=self._output_stream,
            image=self._image,
            command=self._command,
            args=self._args,
            pipeline=self._pipeline,
            env_vars=self._env_vars,
        )


class CreateFunctionParams(FunctionParams):
    def __init__(
        self,
        uuid: str,
        name: str,
        input_stream: str,
        output_stream: str,
        image: str,
        command: list[str],
        args: list[str],
        env_vars: dict[str, str],
        pipeline: PipelineIdentifiers,
    ) -> None:
        super().__init__(
            uuid,
            name,
            input_stream,
            output_stream,
            image,
            command,
            args,
            env_vars,
            pipeline,
        )


class UpdateFunctionParams(FunctionParams):
    def __init__(
        self,
        uuid: str,
        name: str,
        input_stream: str,
        output_stream: str,
        image: str,
        command: list[str],
        args: list[str],
        env_vars: dict[str, str],
        pipeline: PipelineIdentifiers,
    ) -> None:
        super().__init__(
            uuid,
            name,
            input_stream,
            output_stream,
            image,
            command,
            args,
            env_vars,
            pipeline,
        )
