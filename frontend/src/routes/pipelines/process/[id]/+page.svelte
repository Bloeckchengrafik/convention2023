<script lang="ts">
    import type {PageData} from "./$types";
    import type {PipelineWithSampleCount} from "$lib/endpoints";
    import {endpoint} from "$lib/api";
    import {poll} from "$lib/poll";
    import {goto} from "$app/navigation";

    export let data: PageData;

    let pipelinePromise = endpoint<PipelineWithSampleCount>(`pipeline/id/${data.id}`)

    let startedTranfer = false

    poll(async () => {
        let awaited = await endpoint<PipelineWithSampleCount>(`pipeline/id/${data.id}`)
        pipelinePromise = Promise.resolve(awaited)

        if (awaited.status === "BUILDING" && !startedTranfer) {
            startedTranfer = true
            await new Promise(resolve => setTimeout(resolve, 1000))
            await goto(`/pipelines/build/${data.id}`)
        }
    }, 1000);

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
            <span class="step-item active">
                Sample processing
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
                    <h1>Processing Sample for #{data.id}</h1>
                </div>
            </div>
            <div class="card-body d-flex align-items-center justify-content-center flex-column gap-3 p-5">
                {#await pipelinePromise}
                    <p>Waiting for pipeline ...</p>
                {:then sync}
                    <h3>Just a second...</h3>
                    <div class="container-narrow">
                        <div class="progress progress-lg">
                                <div class="progress-bar progress-bar-indeterminate"></div>
                        </div>
                    </div>
                {:catch error}
                    <p>Failed to load pipeline: {error.message}</p>
                {/await}
            </div>
        </div>
    </div>
</div>