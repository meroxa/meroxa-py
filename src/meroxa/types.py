from enum import Enum

class ClientOptions:
    def __init__(self, auth: str, url: str, timeout=0.0):
        self.auth = auth
        self.timeout = timeout
        self.url = url


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
            name = self.name,
            uuid = self.uuid
        )


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
    def __init__(self, address: str, publicKey: str):
        self.address = address
        self.publicKey = publicKey

    def reprJSON(self):
        return dict(address=self.address, publicKey=self.publicKey)


class CreateResourceParams:
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

class UpdateResourceParams:
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
