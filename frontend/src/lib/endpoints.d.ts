export type IndexEndpoint = {
    message: string;
    git_commit_hash: string;
    server_time: string;
    version: string;
};

export type PipelineStatus = 'pending' | 'processable' | 'processing' | 'cutting' | 'done' | 'error' | 'BUILDING';

export type Pipeline = {
    id: number;
    status: PipelineStatus;
    timestamp: string;
}


export type PipelineWithSampleCount = Pipeline & {
    sample_count: number;
}