export type IndexEndpoint = {
    message: string;
    git_commit_hash: string;
    server_time: string;
    version: string;
};

export type PipelineStatus = 'pending' | 'processable' | 'processing' | 'cutting' | 'done' | 'error';

export type Pipeline = {
    id: number;
    status: PipelineStatus;
    timestamp: string;
}


export type PipelineWithImageCount = Pipeline & {
    image_count: number;
}