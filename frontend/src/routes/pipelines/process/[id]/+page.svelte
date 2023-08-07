<script lang="ts">
    import type {PageData} from "./$types";
    import type {PipelineWithImageCount} from "$lib/endpoints";
    import {endpoint} from "$lib/api";
    import {poll} from "$lib/poll";

    export let data: PageData;

    let pipelinePromise = endpoint<PipelineWithImageCount>(`pipeline/id/${data.id}`)

    poll(async () => {
        let awaited = await endpoint<PipelineWithImageCount>(`pipeline/id/${data.id}`)
        pipelinePromise = Promise.resolve(awaited)
    }, 1000);

</script>

<div class="h-full row">
    <div class="column d-flex flex-column">
        <div class="steps">
            <span class="step-item">
                Pipeline creation
            </span>
            <span class="step-item">
                Image capturing
            </span>
            <span class="step-item active">
                Image processing
            </span>
            <span class="step-item">
                Model building
            </span>
            <span class="step-item">
                Cutting
            </span>
        </div>
        <div class="card mt-4 flex-grow-1">
            <div class="card-header">
                <div class="card-title">
                    <h1>Processing Images for #{data.id}</h1>
                </div>
            </div>
            <div class="card-body d-flex align-items-center justify-content-center flex-column gap-3 p-5">
                {#await pipelinePromise}
                    <p>Waiting for pipeline ...</p>
                {:then pipelineSync}
                    <h3>Capturing images: <span class="text-capitalize status status-green">{pipelineSync.status}</span>
                    </h3>
                    <div class="container-narrow">
                        <div class="progress progress-lg">
                                <div class="progress-bar progress-bar-indeterminate"></div>
                        </div>
                    </div>
                    <br/>
                    <p>Images captured: <b>{pipelineSync.image_count}</b></p>
                {:catch error}
                    <p>Failed to load pipeline: {error.message}</p>
                {/await}
            </div>
        </div>
    </div>
</div>