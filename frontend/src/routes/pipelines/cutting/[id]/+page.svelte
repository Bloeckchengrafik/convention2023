<script lang="ts">
    import type {PageData} from "../../../../../.svelte-kit/types/src/routes";
    import type {PipelineWithSampleCount} from "$lib/endpoints";
    import {endpoint} from "$lib/api";
    import {poll} from "$lib/poll";

    export let data: PageData;

    let pipelinePromise = endpoint<PipelineWithSampleCount>(`pipeline/id/${data.id}`)

    poll(async () => {
        let awaited = await endpoint<PipelineWithSampleCount>(`pipeline/id/${data.id}`)
        pipelinePromise = Promise.resolve(awaited)
    }, 1000);


    $: (async () => {
        let pipeline = await pipelinePromise
        if (pipeline.status === "done") {
            window.location.href = `/`
        }
    })()
</script>

<div class="h-full row">
    <div class="column d-flex flex-column">
        <div class="steps">
            <span class="step-item">
                Pipeline creation
            </span>
            <span class="step-item">
                Sample capturing
            </span>
            <span class="step-item">
                Sample processing
            </span>
            <span class="step-item">
                Model building
            </span>
            <span class="step-item active">
                Cutting
            </span>
        </div>
        <div class="card mt-4 flex-grow-1">
            <div class="card-header">
                <div class="card-title">
                    <h1>Capturing Samples for #{data.id} (Mode: {data.env})</h1>
                </div>
            </div>
            <div class="card-body d-flex align-items-center justify-content-center flex-column gap-3 p-5">
                {#await pipelinePromise}
                    <p>Waiting for pipeline ...</p>
                {:then pipelineSync}
                    <h3>Current Step: <span
                            class="text-capitalize status status-green">{pipelineSync.status}</span>
                    </h3>
                    <div class="container-narrow">
                        <div class="progress progress-lg">
                            <div class="progress-bar progress-bar-indeterminate"></div>
                        </div>
                    </div>
                    <br/>
                    <p>Please wait</p>
                {:catch error}
                    <p>Failed to load pipeline: {error.message}</p>
                {/await}
            </div>
        </div>
    </div>
</div>