// Generated by https://quicktype.io

export interface DocumentResult {
    statusCode: number;
    res: Document[];
}

export interface Document {
    Form: string;
    Text: string;
    Data: string;
    S3Record: S3Record;
    Bucket: string;
    Key: string;
}

export interface S3Record {
    s3: S3;
    awsRegion: string;
    eventVersion: string;
    responseElements: ResponseElements;
    eventSource: string;
    eventTime: string;
    requestParameters: RequestParameters;
    eventName: string;
    userIdentity: ErIdentity;
}

export interface RequestParameters {
    sourceIPAddress: string;
}

export interface ResponseElements {
    'x-amz-id-2': string;
    'x-amz-request-id': string;
}

export interface S3 {
    bucket: Bucket;
    configurationId: string;
    s3SchemaVersion: string;
    object: Object;
}

export interface Bucket {
    name: string;
    arn: string;
    ownerIdentity: ErIdentity;
}

export interface ErIdentity {
    principalId: string;
}

export interface Object {
    eTag: string;
    size: number;
    key: string;
    sequencer: string;
}