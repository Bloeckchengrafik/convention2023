export type IndexEndpoint = {
    message: string;
    git_commit_hash: string;
    server_time: string;
    version: string;
};

export type PipelineStatus = 'pending' | 'processing' | 'cutting' | 'done' | 'error';

export type Pipeline = {
    id: number;
    status: PipelineStatus;
    timestamp: string;
}