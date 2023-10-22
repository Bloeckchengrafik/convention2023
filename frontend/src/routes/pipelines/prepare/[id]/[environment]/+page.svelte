<script lang="ts">
    import type {PageData} from "./$types";
    import type {PipelineWithSampleCount} from "$lib/endpoints";
    import {endpoint} from "$lib/api";
    import {poll} from "$lib/poll";

    export let data: PageData;

    let pipelinePromise = endpoint<PipelineWithSampleCount>(`pipeline/id/${data.id}`)

    poll(async () => {
        let awaited = await endpoint<PipelineWithSampleCount>(`pipeline/id/${data.id}`)
        pipelinePromise = Promise.resolve(awaited)
    }, 1000);


    (async () => {
        let pipeline = await pipelinePromise
        if (pipeline.status === "pending") {
            // Launch pipeline
            await new Promise(resolve => setTimeout(resolve, 100))
            await endpoint(`scan/p/${data.id}/run?dataset=${data.env}&resolution=5`)
        }
    })()

    let enableCountdown = false
    let countdownPercent = 0

    function getCountup(resolveFn: () => void) {
        function countup() {
            if (countdownPercent < 100) {
                countdownPercent += 10
                setTimeout(countup, 500)
            } else {
                resolveFn()
            }
        }

        return countup
    }

    $: (async () => {
        let pipeline = await pipelinePromise
        if (pipeline.status === "processable" && !enableCountdown) {
            enableCountdown = true
            countdownPercent = 0
            getCountup(async () => {
                await endpoint(`pipeline/id/${data.id}/process`)
                window.location.href = `/pipelines/process/${data.id}`
            })();
        }
    })()
</script>

<div class="h-full row">
    <div class="column d-flex flex-column">
        <div class="steps">
            <span class="step-item">
                Pipeline creation
            </span>
            <span class="step-item active">
                Sample capturing
            </span>
            <span class="step-item">
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
                    <h1>Capturing Samples for #{data.id} (Mode: {data.env})</h1>
                </div>
            </div>
            <div class="card-body d-flex align-items-center justify-content-center flex-column gap-3 p-5">
                {#await pipelinePromise}
                    <p>Waiting for pipeline ...</p>
                {:then pipelineSync}
                    <h3>Capturing samples: <span class="text-capitalize status status-green">{pipelineSync.status}</span>
                    </h3>
                    <div class="container-narrow">
                        <div class="progress progress-lg">
                            {#if enableCountdown}
                                <div class="progress-bar" style="width: {countdownPercent}%"></div>
                            {:else}
                                <div class="progress-bar progress-bar-indeterminate"></div>
                            {/if}
                        </div>
                    </div>
                    <br/>
                    <p>Samples captured: <b>{pipelineSync.sample_count}</b></p>
                {:catch error}
                    <p>Failed to load pipeline: {error.message}</p>
                {/await}
            </div>
        </div>
    </div>
</div>